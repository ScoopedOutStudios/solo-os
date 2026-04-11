"""Reusable GitHub issue/project helpers for Solo OS."""

from __future__ import annotations

import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from solo_os import config

GRAPHQL_PROJECT_ITEMS_ORG = """
query($owner: String!, $number: Int!, $cursor: String) {
  organization(login: $owner) {
    projectV2(number: $number) {
      id
      items(first: 100, after: $cursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          content {
            __typename
            ... on Issue {
              number
              title
              body
              url
              state
              repository {
                nameWithOwner
              }
            }
          }
          fieldValues(first: 20) {
            nodes {
              __typename
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field {
                  ... on ProjectV2SingleSelectField {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
""".strip()

GRAPHQL_PROJECT_ITEMS_USER = """
query($owner: String!, $number: Int!, $cursor: String) {
  user(login: $owner) {
    projectV2(number: $number) {
      id
      items(first: 100, after: $cursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          content {
            __typename
            ... on Issue {
              number
              title
              body
              url
              state
              repository {
                nameWithOwner
              }
            }
          }
          fieldValues(first: 20) {
            nodes {
              __typename
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field {
                  ... on ProjectV2SingleSelectField {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
""".strip()


@dataclass
class ProjectIssueItem:
    item_id: str
    project_id: str
    repo: str
    number: int
    title: str
    body: str
    url: str
    state: str
    kind: str
    status: str
    stage: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "project_id": self.project_id,
            "repo": self.repo,
            "number": self.number,
            "title": self.title,
            "body": self.body,
            "url": self.url,
            "state": self.state,
            "kind": self.kind,
            "status": self.status,
            "stage": self.stage,
        }


def _run_gh(args: list[str], input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["gh", *args],
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "gh command failed")
    return proc


def run_gh_json(args: list[str], input_text: str | None = None) -> Any:
    proc = _run_gh(args, input_text=input_text)
    return json.loads(proc.stdout)


def run_gh_text(args: list[str], input_text: str | None = None) -> str:
    proc = _run_gh(args, input_text=input_text)
    return proc.stdout.strip()


def get_project_config(root: Path | None = None) -> dict[str, Any]:
    return config.project_config(root)


def get_repo_alias_map(root: Path | None = None) -> dict[str, str]:
    return config.repo_alias_map(root)


def resolve_repo(repo: str, root: Path | None = None) -> str:
    value = repo.strip()
    aliases = get_repo_alias_map(root)
    return aliases.get(value, value)


def _graphql_query(owner_type: str) -> str:
    if owner_type == "user":
        return GRAPHQL_PROJECT_ITEMS_USER
    return GRAPHQL_PROJECT_ITEMS_ORG


def _extract_project_from_payload(payload: dict[str, Any], owner_type: str) -> dict[str, Any] | None:
    data = payload.get("data") or {}
    if owner_type == "user":
        owner_obj = data.get("user") or {}
    else:
        owner_obj = data.get("organization") or {}
    return owner_obj.get("projectV2")


def gh_project_metadata(cfg: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    project = run_gh_json(
        [
            "project",
            "view",
            str(cfg["number"]),
            "--owner",
            str(cfg["owner"]),
            "--format",
            "json",
        ]
    )
    fields = run_gh_json(
        [
            "project",
            "field-list",
            str(cfg["number"]),
            "--owner",
            str(cfg["owner"]),
            "--format",
            "json",
        ]
    )
    return str(project["id"]), fields


def field_and_option_ids(fields_json: dict[str, Any], field_name: str, option_name: str) -> tuple[str, str]:
    for field in fields_json.get("fields", []):
        if field.get("name") != field_name:
            continue
        field_id = str(field["id"])
        for option in field.get("options", []):
            if option.get("name") == option_name:
                return field_id, str(option["id"])
    raise RuntimeError(f"Could not resolve {field_name} option '{option_name}'")


def _extract_single_select_values(field_nodes: list[dict[str, Any]]) -> dict[str, str]:
    values: dict[str, str] = {}
    for node in field_nodes:
        if node.get("__typename") != "ProjectV2ItemFieldSingleSelectValue":
            continue
        field = node.get("field") or {}
        field_name = field.get("name")
        option_name = node.get("name")
        if field_name and option_name:
            values[str(field_name)] = str(option_name)
    return values


def infer_kind_from_title(title: str) -> str:
    if title.startswith("[") and "]" in title:
        raw_kind = title[1 : title.index("]")].strip()
        return normalize_kind(raw_kind)
    return ""


def normalize_kind(kind: str) -> str:
    normalized = kind.strip()
    if normalized in {"Initiative", "Ops"}:
        return "Build Loop"
    return normalized


def list_project_items(
    cfg: dict[str, Any],
    *,
    repo: str | None = None,
    kind: str | None = None,
    status: str | None = None,
    state: str = "OPEN",
    search: str | None = None,
    root: Path | None = None,
) -> list[ProjectIssueItem]:
    resolved_repo = resolve_repo(repo, root) if repo else None
    owner_type = str(cfg.get("owner_type", "org"))
    query = _graphql_query(owner_type)
    cursor: str | None = None
    items: list[ProjectIssueItem] = []

    while True:
        query_args = [
            "api",
            "graphql",
            "-f",
            f"query={query}",
            "-F",
            f"owner={cfg['owner']}",
            "-F",
            f"number={cfg['number']}",
        ]
        if cursor is not None:
            query_args.extend(["-F", f"cursor={cursor}"])
        payload = run_gh_json(query_args)

        project = _extract_project_from_payload(payload, owner_type)
        if project is None:
            raise RuntimeError("Could not load project items from GitHub")

        project_id = str(project["id"])
        batch = project["items"]["nodes"]
        for node in batch:
            content = node.get("content") or {}
            if content.get("__typename") != "Issue":
                continue
            repo_name = str((content.get("repository") or {}).get("nameWithOwner") or "")
            issue_state = str(content.get("state") or "")
            field_values = _extract_single_select_values(
                (node.get("fieldValues") or {}).get("nodes") or []
            )
            stage_field = str(cfg.get("stageFieldName") or "Stage")
            item = ProjectIssueItem(
                item_id=str(node["id"]),
                project_id=project_id,
                repo=repo_name,
                number=int(content["number"]),
                title=str(content["title"]),
                body=str(content.get("body") or ""),
                url=str(content["url"]),
                state=issue_state,
                kind=normalize_kind(
                    str(
                        field_values.get(str(cfg["kindFieldName"]))
                        or infer_kind_from_title(str(content["title"]))
                    )
                ),
                status=str(field_values.get(str(cfg["statusFieldName"])) or ""),
                stage=str(field_values.get(stage_field) or ""),
            )

            if resolved_repo and item.repo != resolved_repo:
                continue
            if kind and item.kind != kind:
                continue
            if status and item.status != status:
                continue
            if state.lower() != "all" and item.state.lower() != state.lower():
                continue
            if search:
                haystack = f"{item.title}\n{item.body}".lower()
                if search.lower() not in haystack:
                    continue
            items.append(item)

        page_info = project["items"]["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = str(page_info["endCursor"])

    return items


def get_project_item(
    cfg: dict[str, Any],
    *,
    repo: str,
    number: int,
    root: Path | None = None,
) -> ProjectIssueItem | None:
    matches = list_project_items(cfg, repo=repo, state="all", root=root)
    for item in matches:
        if item.number == number:
            return item
    return None


def issue_view(repo: str, number: int) -> dict[str, Any]:
    return run_gh_json(
        [
            "issue",
            "view",
            str(number),
            "--repo",
            repo,
            "--json",
            "number,title,body,url,state",
        ]
    )


def edit_issue(
    repo: str,
    number: int,
    *,
    title: str | None = None,
    body: str | None = None,
) -> None:
    args = ["issue", "edit", str(number), "--repo", repo]
    if title is not None:
        args.extend(["--title", title])
    if body is not None:
        args.extend(["--body-file", "-"])
    run_gh_text(args, input_text=body)


def comment_on_issue(repo: str, number: int, comment: str) -> None:
    run_gh_text(
        ["issue", "comment", str(number), "--repo", repo, "--body-file", "-"],
        input_text=comment,
    )


def close_issue(repo: str, number: int, *, reason: str = "completed") -> None:
    run_gh_text(["issue", "close", str(number), "--repo", repo, "--reason", reason])


def add_issue_to_project(owner: str, number: int, issue_url: str) -> dict[str, Any]:
    last_error: RuntimeError | None = None
    for _ in range(6):
        try:
            return run_gh_json(
                [
                    "project",
                    "item-add",
                    str(number),
                    "--owner",
                    owner,
                    "--url",
                    issue_url,
                    "--format",
                    "json",
                ]
            )
        except RuntimeError as exc:
            last_error = exc
            time.sleep(1.0)
    if last_error is not None:
        raise last_error
    raise RuntimeError(f"Failed to add project item for {issue_url}")


def set_single_select(project_id: str, item_id: str, field_id: str, option_id: str) -> None:
    run_gh_text(
        [
            "project",
            "item-edit",
            "--id",
            item_id,
            "--project-id",
            project_id,
            "--field-id",
            field_id,
            "--single-select-option-id",
            option_id,
        ]
    )


def ensure_project_item(cfg: dict[str, Any], repo: str, number: int) -> ProjectIssueItem:
    item = get_project_item(cfg, repo=repo, number=number)
    if item is not None:
        return item

    issue = issue_view(repo, number)
    add_issue_to_project(str(cfg["owner"]), int(cfg["number"]), str(issue["url"]))
    for _ in range(6):
        refreshed = get_project_item(cfg, repo=repo, number=number)
        if refreshed is not None:
            return refreshed
        time.sleep(1.0)
    raise RuntimeError(f"Added issue to project but could not find project item for {repo}#{number}")


def update_project_fields(
    cfg: dict[str, Any],
    repo: str,
    number: int,
    *,
    kind: str | None = None,
    status: str | None = None,
    stage: str | None = None,
) -> None:
    if kind is None and status is None and stage is None:
        return

    project_id, fields_json = gh_project_metadata(cfg)
    item = ensure_project_item(cfg, repo, number)

    if kind is not None:
        field_id, option_id = field_and_option_ids(fields_json, str(cfg["kindFieldName"]), kind)
        set_single_select(project_id, item.item_id, field_id, option_id)
    if status is not None:
        field_id, option_id = field_and_option_ids(fields_json, str(cfg["statusFieldName"]), status)
        set_single_select(project_id, item.item_id, field_id, option_id)
    if stage is not None:
        stage_field = str(cfg.get("stageFieldName") or "Stage")
        field_id, option_id = field_and_option_ids(fields_json, stage_field, stage)
        set_single_select(project_id, item.item_id, field_id, option_id)
