### 2.0.34

#### Bugfixes:
- Fixed a bug with non-ascii project names using the package with Python 2.
- Fixed a bug (affecting Python 2 only) with printing projects and features whose names are
  not ascii.
- Fixed a bug with project creation from non-ascii file names. Project creation from non-ascii file names
  is not supported, so this now raises a more informative exception. The project name is no longer used as 
  the file name in cases where we do not have a file name, which prevents non-ascii project names from
  causing problems in those circumstances.

### 2.0.32
#### API Changes
- The name of the package has been changed to `datarobot`
- An alias for ``Project.get_jobs`` called ``get_model_jobs`` has been
  added to the ``Project`` class. This rename has already taken place
  in releases 2.1 and 2.2; adding it here will make it easier to maintain
  this version.

### 2.0.31
#### Bugfixes
In Python 2, using a unicode token to instantiate the client will
now work correctly.

### 2.0.30
#### Bugfixes
The minimum required version of ``trafaret`` has been upgraded to 0.7.1
to avoid a compatibility issue between it and a new version of ``setuptools``.

### 2.0.29
#### Bugfixes
The minimum version of ``requests-toolbelt`` has been upgraded to 0.6
to avoid an issue that would sometimes cause connection errors

### 2.0.28
#### Enhancements
The minimum versions of all dependencies have been specified, rather than
one specific version. This will make it easier to have the package installed
alongside other packages in the same virtualenv.

### 2.0.27

#### New features
- ``PredictJob`` class was added to work with prediction jobs
- ``wait_for_async_predictions`` function added to `predict_job` module

#### Deprecation Summary:
- The `order_by` parameter of the ``Project.list`` is now deprecated.


### 0.2.26

#### New features
- None

#### Enhancements
- ``Projet.set_target`` will re-fetch the project data after it succeeds,
  keeping the client side in sync with the state of the project on the
  server
- ``Project.create_featurelist`` now throws ``DuplicateFeaturesError``
  exception if passed list of features contains duplicates
- ``Project.get_models`` now supports snake_case arguments to its
  order_by keyword

#### Deprecation Summary:
- ``Project.wait_for_aim_stage`` is now deprecated, as the REST Async
flow is a more reliable method of determining that project creation has
completed successfully
- ``Project.status`` is deprecated in favor of ``Project.get_status``
- ``recommendation_settings`` parameter of ``Project.start`` is
  deprecated in favor of ``recommender_settings``

#### Bugfixes
- ``Project.wait_for_aim_stage`` changed to support Python 3
- Fixed incorrect value of ``SCORING_TYPE.cross_validation``
- Models returned by ``Project.get_models`` will now be correctly
  ordered when the order_by keyword is used

#### API Changes
- None


### 0.2.25

- Pinned versions of required libraries

### 0.2.24

Official release of v0.2

### 0.1.24

- Updated documentation
- Renamed parameter `name` of `Project.create` and `Project.start` to `project_name`
- Removed `Model.predict` method
- `wait_for_async_model_creation` function added to `modeljob` module
- `wait_for_async_status_service` of `Project` class renamed to `_wait_for_async_status_service`
- Can now use auth_token in config file to configure SDK

### 0.1.23

- Fixes a method that pointed to a removed route

### 0.1.22

- Added `featurelist_id` attribute to `ModelJob` class

### 0.1.21

- Removes `model` attribute from `ModelJob` class

### 0.1.20

- Project creation raises `AsyncProjectCreationError` if it was unsuccessful
- Removed `Model.list_prime_rulesets` and `Model.get_prime_ruleset` methods
- Removed `Model.predict_batch` method
- Removed `Project.create_prime_model` method
- Removed `PrimeRuleSet` model
- Adds backwards compatibility bridge for ModelJob async
- Adds ModelJob.get and ModelJob.get_model

### 0.1.19:

- Minor bugfixes in `wait_for_async_status_service`

### 0.1.18:

- Removes `submit_model` from Project until serverside implementation is improved
- Switches training URLs for new resource-based route at /projects/<project_id>/models/
- Job renamed to ModelJob, and using modelJobs route
- Fixes an inconsistency in argument order for `train` methods

### 0.1.17:

- `wait_for_async_status_service` timeout increased from 60s to 600s

### 0.1.16:

- `Project.create` will now handle both async/sync project creation

### 0.1.15:

- All routes pluralized to sync with changes in API
- `Project.get_jobs` will request all jobs when no param specified
- dataframes from `predict` method will have pythonic names
- `Project.get_status` created, `Project.status` now deprecated
- `Project.unlock_holdout` created.
- Added `quickrun` parameter to `Project.set_target`
- Added `modelCategory` to Model schema
- Add `permalinks` featrue to Project and Model objects.
- `Project.create_prime_model` created

### 0.1.14:

- `Project.set_worker_count` fix for compatibility with API change in project update.

### 0.1.13:

- Add positive class to `set_target`.
- Change attributes names of `Project`, `Model`, `Job` and `Blueprint`
    - `features` in `Model`, `Job` and `Blueprint` are now `processes`
    - `dataset_id` and `dataset_name` migrated to `featurelist_id` and `featurelist_name`.
    - `samplepct` -> `sample_pct`
- `Model` has now `blueprint`, `project`, and `featurlist` attributes.
- Minor bugfixes.

### 0.1.12:
- Minor fixes regarding rename `Job` attributes. `features` attributes now named `processes`, `samplepct` now is `sample_pct`.


### 0.1.11:

(May 27, 2015):

- Minor fixes regarding migrating API from under_score names to camelCase.

### 0.1.10 :

(May 20, 2015):

- Remove `Project.upload_file`, `Project.upload_file_from_url` and `Project.attach_file` methods. Moved all logic that uploading file to `Project.create` method. 

### 0.1.9
(May 15, 2015)
- Fix uploading file causing a lot of memory usage. Minor bugfixes.
