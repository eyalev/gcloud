"""Generated message classes for source version v1.

Access source code repositories hosted by Google.
"""
# NOTE: This file is autogenerated and should not be edited by hand.

from googlecloudsdk.third_party.apitools.base.protorpclite import messages as _messages
from googlecloudsdk.third_party.apitools.base.py import encoding


package = 'source'


class Action(_messages.Message):
  """An action to perform on a path in a workspace.

  Fields:
    copyAction: Copy the contents of one path to another.
    deleteAction: Delete a file or directory.
    writeAction: Create or modify a file.
  """

  copyAction = _messages.MessageField('CopyAction', 1)
  deleteAction = _messages.MessageField('DeleteAction', 2)
  writeAction = _messages.MessageField('WriteAction', 3)


class ChangedFileInfo(_messages.Message):
  """Represents file information.

  Enums:
    OperationValueValuesEnum: The operation type for the file.

  Fields:
    fromPath: Related file path for copies or renames.  For copies, the type
      will be ADDED and the from_path will point to the source of the copy.
      For renames, the type will be ADDED, the from_path will point to the
      source of the rename, and another ChangedFileInfo record with that path
      will appear with type DELETED. In other words, a rename is represented
      as a copy plus a delete of the old path.
    hash: A hex-encoded hash for the file. Not necessarily a hash of the
      file's contents. Two paths in the same revision with the same hash have
      the same contents with high probability. Empty if the operation is
      CONFLICTED.
    operation: The operation type for the file.
    path: The path of the file.
  """

  class OperationValueValuesEnum(_messages.Enum):
    """The operation type for the file.

    Values:
      OPERATION_UNSPECIFIED: No operation was specified.
      ADDED: The file was added.
      DELETED: The file was deleted.
      MODIFIED: The file was modified.
      CONFLICTED: The result of merging the file is a conflict. The CONFLICTED
        type only appears in Workspace.changed_files or Snapshot.changed_files
        when the workspace is in a merge state.
    """
    OPERATION_UNSPECIFIED = 0
    ADDED = 1
    DELETED = 2
    MODIFIED = 3
    CONFLICTED = 4

  fromPath = _messages.StringField(1)
  hash = _messages.StringField(2)
  operation = _messages.EnumField('OperationValueValuesEnum', 3)
  path = _messages.StringField(4)


class CloudWorkspaceId(_messages.Message):
  """A CloudWorkspaceId is a unique identifier for a cloud workspace. A cloud
  workspace is a place associated with a repo where modified files can be
  stored before they are committed.

  Fields:
    name: The unique name of the workspace within the repo.  This is the name
      chosen by the client in the Source API's CreateWorkspace method.
    repoId: The ID of the repo containing the workspace.
  """

  name = _messages.StringField(1)
  repoId = _messages.MessageField('RepoId', 2)


class CopyAction(_messages.Message):
  """Copy the contents of a file or directory at from_path in the specified
  revision or snapshot to to_path.  To rename a file, copy it to the new path
  and delete the old.

  Fields:
    fromPath: The path to copy from.
    fromRevisionId: The revision ID from which to copy the file.
    fromSnapshotId: The snapshot ID from which to copy the file.
    toPath: The path to copy to.
  """

  fromPath = _messages.StringField(1)
  fromRevisionId = _messages.StringField(2)
  fromSnapshotId = _messages.StringField(3)
  toPath = _messages.StringField(4)


class CreateWorkspaceRequest(_messages.Message):
  """Request for CreateWorkspace.

  Fields:
    actions: An ordered sequence of actions to perform in the workspace. Can
      be empty. Specifying actions here instead of using ModifyWorkspace saves
      one RPC.
    repoId: The repo within which to create the workspace.
    workspace: The following fields of workspace, with the allowable exception
      of baseline, must be set. No other fields of workspace should be set.
      id.name Provides the name of the workspace and must be unique within the
      repo. Note: Do not set field id.repo_id.  The repo_id is provided above
      as a CreateWorkspaceRequest field.  alias: If alias names an existing
      movable alias, the workspace's baseline is set to the alias's revision.
      If alias does not name an existing movable alias, then the workspace is
      created with no baseline. When the workspace is committed, a new root
      revision is created with no parents. The new revision becomes the
      workspace's baseline and the alias name is used to create a movable
      alias referring to the revision.  baseline: A revision ID (hexadecimal
      string) for sequencing. If non-empty, alias must name an existing
      movable alias and baseline must match the alias's revision ID.
  """

  actions = _messages.MessageField('Action', 1, repeated=True)
  repoId = _messages.MessageField('RepoId', 2)
  workspace = _messages.MessageField('Workspace', 3)


class DeleteAction(_messages.Message):
  """Delete a file or directory.

  Fields:
    path: The path of the file or directory. If path refers to a directory,
      the directory and its contents are deleted.
  """

  path = _messages.StringField(1)


class Empty(_messages.Message):
  """A generic empty message that you can re-use to avoid defining duplicated
  empty messages in your APIs. A typical example is to use it as the request
  or the response type of an API method. For instance:      service Foo {
  rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);     }  The
  JSON representation for `Empty` is empty JSON object `{}`.
  """



class ListReposResponse(_messages.Message):
  """Response for ListRepos.

  Fields:
    repos: The listed repos.
  """

  repos = _messages.MessageField('Repo', 1, repeated=True)


class ListWorkspacesResponse(_messages.Message):
  """Response for ListWorkspaces.

  Fields:
    workspaces: The listed workspaces.
  """

  workspaces = _messages.MessageField('Workspace', 1, repeated=True)


class MergeInfo(_messages.Message):
  """MergeInfo holds information needed while resolving merges, and refreshes
  that involve conflicts.

  Fields:
    commonAncestorRevisionId: Revision ID of the closest common ancestor of
      the file trees that are participating in a refresh or merge.  During a
      refresh, the common ancestor is the baseline of the workspace.  During a
      merge of two branches, the common ancestor is derived from the workspace
      baseline and the alias of the branch being merged in.  The repository
      state at the common ancestor provides the base version for a three-way
      merge.
    isRefresh: If true, a refresh operation is in progress.  If false, a merge
      is in progress.
    otherRevisionId: During a refresh, the ID of the revision with which the
      workspace is being refreshed. This is the revision ID to which the
      workspace's alias refers at the time of the RefreshWorkspace call.
      During a merge, the ID of the revision that's being merged into the
      workspace's alias. This is the revision_id field of the MergeRequest.
    workspaceAfterSnapshotId: The workspace snapshot immediately after the
      refresh or merge RPC completes.  If a file has conflicts, this snapshot
      contains the version of the file with conflict markers.
    workspaceBeforeSnapshotId: During a refresh, the snapshot ID of the latest
      change to the workspace before the refresh.  During a merge, the
      workspace's baseline, which is identical to the commit hash of the
      workspace's alias before initiating the merge.
  """

  commonAncestorRevisionId = _messages.StringField(1)
  isRefresh = _messages.BooleanField(2)
  otherRevisionId = _messages.StringField(3)
  workspaceAfterSnapshotId = _messages.StringField(4)
  workspaceBeforeSnapshotId = _messages.StringField(5)


class ModifyWorkspaceRequest(_messages.Message):
  """Request for ModifyWorkspace.

  Fields:
    actions: An ordered sequence of actions to perform in the workspace.  May
      not be empty.
    currentSnapshotId: If non-empty, current_snapshot_id must refer to the
      most recent update to the workspace, or ABORTED is returned.
    workspaceId: The ID of the workspace.
  """

  actions = _messages.MessageField('Action', 1, repeated=True)
  currentSnapshotId = _messages.StringField(2)
  workspaceId = _messages.MessageField('CloudWorkspaceId', 3)


class ProjectRepoId(_messages.Message):
  """Selects a repo using a Google Cloud Platform project ID (e.g. winged-
  cargo-31) and a repo name within that project.
  """



class Repo(_messages.Message):
  """A repository (or repo) stores files for a version-control system.

  Enums:
    StateValueValuesEnum: The state the repo is in.
    VcsValueValuesEnum: The version control system of the repo.

  Fields:
    createTime: Timestamp when the repo was created.
    id: Randomly generated ID that uniquely identifies a repo.
    name: Human-readable, user-defined name of the repository. Names must be
      alphanumeric, lowercase, begin with a letter, and be between 3 and 63
      characters long. The - character can appear in the middle positions.
      (Names must satisfy the regular expression a-z{1,61}[a-z0-9].)
    projectId: Immutable, globally unique, DNS-compatible textual identifier.
      Examples: user-chosen-project-id, yellow-banana-33.
    repoSyncConfig: How RepoSync is configured for this repo. If missing, this
      repo is not set up for RepoSync.
    state: The state the repo is in.
    vcs: The version control system of the repo.
  """

  class StateValueValuesEnum(_messages.Enum):
    """The state the repo is in.

    Values:
      STATE_UNSPECIFIED: No state was specified.
      LIVE: The repo is live and available for use.
      DELETED: The repo has been deleted.
    """
    STATE_UNSPECIFIED = 0
    LIVE = 1
    DELETED = 2

  class VcsValueValuesEnum(_messages.Enum):
    """The version control system of the repo.

    Values:
      VCS_UNSPECIFIED: No version control system was specified.
      GIT: The Git version control system.
    """
    VCS_UNSPECIFIED = 0
    GIT = 1

  createTime = _messages.StringField(1)
  id = _messages.StringField(2)
  name = _messages.StringField(3)
  projectId = _messages.StringField(4)
  repoSyncConfig = _messages.MessageField('RepoSyncConfig', 5)
  state = _messages.EnumField('StateValueValuesEnum', 6)
  vcs = _messages.EnumField('VcsValueValuesEnum', 7)


class RepoId(_messages.Message):
  """A unique identifier for a cloud repo.

  Fields:
    projectRepoId: A combination of a project ID and a repo name.
    uid: A server-assigned, globally unique identifier.
  """

  projectRepoId = _messages.MessageField('ProjectRepoId', 1)
  uid = _messages.StringField(2)


class RepoSyncConfig(_messages.Message):
  """RepoSync configuration information.

  Enums:
    StatusValueValuesEnum: The status of RepoSync.

  Fields:
    externalRepoUrl: If this repo is enabled for RepoSync, this will be the
      URL of the external repo that this repo should sync with.
    status: The status of RepoSync.
  """

  class StatusValueValuesEnum(_messages.Enum):
    """The status of RepoSync.

    Values:
      REPO_SYNC_STATUS_UNSPECIFIED: No RepoSync status was specified.
      OK: RepoSync is working.
      FAILED_AUTH: RepoSync failed because of authorization/authentication.
      FAILED_OTHER: RepoSync failed for a reason other than auth.
      FAILED_NOT_FOUND: RepoSync failed because the repository was not found.
    """
    REPO_SYNC_STATUS_UNSPECIFIED = 0
    OK = 1
    FAILED_AUTH = 2
    FAILED_OTHER = 3
    FAILED_NOT_FOUND = 4

  externalRepoUrl = _messages.StringField(1)
  status = _messages.EnumField('StatusValueValuesEnum', 2)


class SourceProjectsReposDeleteRequest(_messages.Message):
  """A SourceProjectsReposDeleteRequest object.

  Fields:
    projectId: The ID of the project.
    repoName: The name of the repo. Leave empty for the default repo.
    uid: A server-assigned, globally unique identifier.
  """

  projectId = _messages.StringField(1, required=True)
  repoName = _messages.StringField(2, required=True)
  uid = _messages.StringField(3)


class SourceProjectsReposGetRequest(_messages.Message):
  """A SourceProjectsReposGetRequest object.

  Fields:
    projectId: The ID of the project.
    repoName: The name of the repo. Leave empty for the default repo.
    uid: A server-assigned, globally unique identifier.
  """

  projectId = _messages.StringField(1, required=True)
  repoName = _messages.StringField(2, required=True)
  uid = _messages.StringField(3)


class SourceProjectsReposListRequest(_messages.Message):
  """A SourceProjectsReposListRequest object.

  Fields:
    projectId: The project ID whose repos should be listed.
  """

  projectId = _messages.StringField(1, required=True)


class SourceProjectsReposUpdateRequest(_messages.Message):
  """A SourceProjectsReposUpdateRequest object.

  Fields:
    projectId: The ID of the project.
    repoName: The name of the repo. Leave empty for the default repo.
    updateRepoRequest: A UpdateRepoRequest resource to be passed as the
      request body.
  """

  projectId = _messages.StringField(1, required=True)
  repoName = _messages.StringField(2, required=True)
  updateRepoRequest = _messages.MessageField('UpdateRepoRequest', 3)


class SourceProjectsReposWorkspacesCreateRequest(_messages.Message):
  """A SourceProjectsReposWorkspacesCreateRequest object.

  Fields:
    createWorkspaceRequest: A CreateWorkspaceRequest resource to be passed as
      the request body.
    projectId: The ID of the project.
    repoName: The name of the repo. Leave empty for the default repo.
  """

  createWorkspaceRequest = _messages.MessageField('CreateWorkspaceRequest', 1)
  projectId = _messages.StringField(2, required=True)
  repoName = _messages.StringField(3, required=True)


class SourceProjectsReposWorkspacesDeleteRequest(_messages.Message):
  """A SourceProjectsReposWorkspacesDeleteRequest object.

  Fields:
    currentSnapshotId: If non-empty, current_snapshot_id must refer to the
      most recent update to the workspace, or ABORTED is returned.
    name: The unique name of the workspace within the repo.  This is the name
      chosen by the client in the Source API's CreateWorkspace method.
    projectId: The ID of the project.
    repoName: The name of the repo. Leave empty for the default repo.
    uid: A server-assigned, globally unique identifier.
  """

  currentSnapshotId = _messages.StringField(1)
  name = _messages.StringField(2, required=True)
  projectId = _messages.StringField(3, required=True)
  repoName = _messages.StringField(4, required=True)
  uid = _messages.StringField(5)


class SourceProjectsReposWorkspacesGetRequest(_messages.Message):
  """A SourceProjectsReposWorkspacesGetRequest object.

  Fields:
    name: The unique name of the workspace within the repo.  This is the name
      chosen by the client in the Source API's CreateWorkspace method.
    projectId: The ID of the project.
    repoName: The name of the repo. Leave empty for the default repo.
    uid: A server-assigned, globally unique identifier.
  """

  name = _messages.StringField(1, required=True)
  projectId = _messages.StringField(2, required=True)
  repoName = _messages.StringField(3, required=True)
  uid = _messages.StringField(4)


class SourceProjectsReposWorkspacesListRequest(_messages.Message):
  """A SourceProjectsReposWorkspacesListRequest object.

  Enums:
    ViewValueValuesEnum: Specifies which parts of the Workspace resource
      should be returned in the response.

  Fields:
    projectId: The ID of the project.
    repoName: The name of the repo. Leave empty for the default repo.
    uid: A server-assigned, globally unique identifier.
    view: Specifies which parts of the Workspace resource should be returned
      in the response.
  """

  class ViewValueValuesEnum(_messages.Enum):
    """Specifies which parts of the Workspace resource should be returned in
    the response.

    Values:
      STANDARD: <no description>
      MINIMAL: <no description>
      FULL: <no description>
    """
    STANDARD = 0
    MINIMAL = 1
    FULL = 2

  projectId = _messages.StringField(1, required=True)
  repoName = _messages.StringField(2, required=True)
  uid = _messages.StringField(3)
  view = _messages.EnumField('ViewValueValuesEnum', 4)


class SourceProjectsReposWorkspacesModifyWorkspaceRequest(_messages.Message):
  """A SourceProjectsReposWorkspacesModifyWorkspaceRequest object.

  Fields:
    modifyWorkspaceRequest: A ModifyWorkspaceRequest resource to be passed as
      the request body.
    name: The unique name of the workspace within the repo.  This is the name
      chosen by the client in the Source API's CreateWorkspace method.
    projectId: The ID of the project.
    repoName: The name of the repo. Leave empty for the default repo.
  """

  modifyWorkspaceRequest = _messages.MessageField('ModifyWorkspaceRequest', 1)
  name = _messages.StringField(2, required=True)
  projectId = _messages.StringField(3, required=True)
  repoName = _messages.StringField(4, required=True)


class StandardQueryParameters(_messages.Message):
  """Query parameters accepted by all methods.

  Enums:
    FXgafvValueValuesEnum: V1 error format.
    AltValueValuesEnum: Data format for response.

  Fields:
    f__xgafv: V1 error format.
    access_token: OAuth access token.
    alt: Data format for response.
    bearer_token: OAuth bearer token.
    callback: JSONP
    fields: Selector specifying which fields to include in a partial response.
    key: API key. Your API key identifies your project and provides you with
      API access, quota, and reports. Required unless you provide an OAuth 2.0
      token.
    oauth_token: OAuth 2.0 token for the current user.
    pp: Pretty-print response.
    prettyPrint: Returns response with indentations and line breaks.
    quotaUser: Available to use for quota purposes for server-side
      applications. Can be any arbitrary string assigned to a user, but should
      not exceed 40 characters.
    trace: A tracing token of the form "token:<tokenid>" to include in api
      requests.
    uploadType: Legacy upload protocol for media (e.g. "media", "multipart").
    upload_protocol: Upload protocol for media (e.g. "raw", "multipart").
  """

  class AltValueValuesEnum(_messages.Enum):
    """Data format for response.

    Values:
      json: Responses with Content-Type of application/json
      media: Media download with context-dependent Content-Type
      proto: Responses with Content-Type of application/x-protobuf
    """
    json = 0
    media = 1
    proto = 2

  class FXgafvValueValuesEnum(_messages.Enum):
    """V1 error format.

    Values:
      _1: v1 error format
      _2: v2 error format
    """
    _1 = 0
    _2 = 1

  f__xgafv = _messages.EnumField('FXgafvValueValuesEnum', 1)
  access_token = _messages.StringField(2)
  alt = _messages.EnumField('AltValueValuesEnum', 3, default=u'json')
  bearer_token = _messages.StringField(4)
  callback = _messages.StringField(5)
  fields = _messages.StringField(6)
  key = _messages.StringField(7)
  oauth_token = _messages.StringField(8)
  pp = _messages.BooleanField(9, default=True)
  prettyPrint = _messages.BooleanField(10, default=True)
  quotaUser = _messages.StringField(11)
  trace = _messages.StringField(12)
  uploadType = _messages.StringField(13)
  upload_protocol = _messages.StringField(14)


class UpdateRepoRequest(_messages.Message):
  """Request for UpdateRepo.

  Fields:
    repoId: The ID of the repo to be updated.
    repoName: Renames the repo. repo_name cannot already be in use by a LIVE
      repo within the project. This field is ignored if left blank or set to
      the empty string. If you want to rename a repo to "default," you need to
      explicitly set that value here.
  """

  repoId = _messages.MessageField('RepoId', 1)
  repoName = _messages.StringField(2)


class Workspace(_messages.Message):
  """A Cloud Workspace stores modified files before they are committed to a
  repo. This message contains metadata. Use the Read or
  ReadFromWorkspaceOrAlias methods to read files from the workspace, and use
  ModifyWorkspace to change files.

  Fields:
    alias: The alias associated with the workspace. When the workspace is
      committed, this alias will be moved to point to the new revision.
    baseline: The revision of the workspace's alias when the workspace was
      created.
    changedFiles: The set of files modified in this workspace.
    currentSnapshotId: If non-empty, current_snapshot_id refers to the most
      recent update to the workspace.
    id: The ID of the workspace.
    mergeInfo: Information needed to manage a refresh or merge operation.
      Present only during a merge (i.e. after a call to Merge) or a call to
      RefreshWorkspace which results in conflicts.
  """

  alias = _messages.StringField(1)
  baseline = _messages.StringField(2)
  changedFiles = _messages.MessageField('ChangedFileInfo', 3, repeated=True)
  currentSnapshotId = _messages.StringField(4)
  id = _messages.MessageField('CloudWorkspaceId', 5)
  mergeInfo = _messages.MessageField('MergeInfo', 6)


class WriteAction(_messages.Message):
  """Create or modify a file.

  Enums:
    ModeValueValuesEnum: The new mode of the file.

  Fields:
    contents: The new contents of the file.
    mode: The new mode of the file.
    path: The path of the file to write.
  """

  class ModeValueValuesEnum(_messages.Enum):
    """The new mode of the file.

    Values:
      FILE_MODE_UNSPECIFIED: No file mode was specified.
      NORMAL: Neither a symbolic link nor executable.
      SYMLINK: A symbolic link.
      EXECUTABLE: An executable.
    """
    FILE_MODE_UNSPECIFIED = 0
    NORMAL = 1
    SYMLINK = 2
    EXECUTABLE = 3

  contents = _messages.BytesField(1)
  mode = _messages.EnumField('ModeValueValuesEnum', 2)
  path = _messages.StringField(3)


encoding.AddCustomJsonFieldMapping(
    StandardQueryParameters, 'f__xgafv', '$.xgafv',
    package=u'source')
encoding.AddCustomJsonEnumMapping(
    StandardQueryParameters.FXgafvValueValuesEnum, '_1', '1',
    package=u'source')
encoding.AddCustomJsonEnumMapping(
    StandardQueryParameters.FXgafvValueValuesEnum, '_2', '2',
    package=u'source')
