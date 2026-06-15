# Plan: Tuition FeeType Config + Fee/FeeGroup Import

## Summary

Total tickets: **8**

Goal:

- Build a **FeeType config page** with full CRUD API and UI.
- Build **Fee/FeeGroup import** using a **Preview + Commit** flow, including backend validation/commit APIs and frontend upload/preview/result UI.

Current state:

- Backend has models: `FeeType`, `Fee`, `FeeGroup`, `FeeDate`.
- Backend already has list APIs:
  - `/tuition/admin/fee/type/list`
  - `/tuition/admin/fee/list`
  - `/tuition/admin/group-by-fee/list`
- Backend does not yet have full CRUD detail APIs for `FeeType`, `Fee`, and `FeeGroup`.
- UI `AdminTuitionPage.vue` already calls `/tuition/admin/fee/detail/{id}`, but backend does not currently expose that route.
- UI already has `ExcelPreviewDialog.vue`, which can be reused for XLSX preview.

## Ticket 1: Backend FeeType CRUD API

Add admin CRUD APIs for `FeeType`.

Endpoints:

- `GET /tuition/admin/fee/type/list`
- `POST /tuition/admin/fee/type/list`
- `GET /tuition/admin/fee/type/detail/<id>`
- `PUT /tuition/admin/fee/type/detail/<id>`
- `DELETE /tuition/admin/fee/type/detail/<id>`

Behavior:

- Fields: `vi_name`, `en_name`, `type`, `order`.
- List supports existing pagination and query-param filters.
- Delete is soft delete: set `deleted=True`.
- Validate `type` is not blank on create/update.
- Default sort: `order`, `-id`.
- Frontend store must refresh FeeType options after create/update/delete.

Acceptance criteria:

- Admin can create, list, view detail, update, and soft-delete FeeType.
- Deleted FeeTypes no longer appear in list/options.
- Invalid blank `type` returns validation error.

## Ticket 2: UI FeeType Config Page

Create a FeeType management page under Config.

Route/UI:

- Route: `/config/fee-type`
- Route name: `Fee Type Config`
- Add Sidebar item under Config.

UI behavior:

- Table columns:
  - ID
  - Vietnamese Name
  - English Name
  - Type
  - Order
  - Actions
- Add/Edit dialog using Quasar form.
- Delete confirmation using existing delete dialog pattern.
- Search/filter by name/type if supported by backend query params.
- After save/delete:
  - Reload list.
  - Call `tuitionStore.getOptions(true)`.

Acceptance criteria:

- User can create/edit/delete FeeType from UI.
- FeeType dropdowns elsewhere refresh after changes.
- Page is accessible from Sidebar Config section.

## Ticket 3: Backend Fee CRUD Detail API

Complete CRUD APIs for `Fee`, especially the detail route currently expected by UI.

Endpoints:

- Existing: `GET /tuition/admin/fee/list`
- Add: `POST /tuition/admin/fee/list`
- Add: `GET /tuition/admin/fee/detail/<id>`
- Add: `PUT /tuition/admin/fee/detail/<id>`
- Add: `DELETE /tuition/admin/fee/detail/<id>`

Payload fields:

- `en_name`
- `vi_name`
- `en_unit`
- `vi_unit`
- `fee_type` mapped to model field `feetype`
- `is_compulsory`
- `is_term`
- `is_quantity`

Behavior:

- Keep response compatible with current `AdminFeeSerializer`, including nested `fee_type`.
- Delete is soft delete.
- Existing `AdminTuitionPage.vue` inline edit must work.

Acceptance criteria:

- Existing Fee inline edit no longer fails due to missing backend route.
- Fee create/update correctly maps `fee_type` to `feetype_id`.
- Deleted Fees no longer appear in admin list.

## Ticket 4: Backend FeeGroup CRUD API

Add admin CRUD APIs for `FeeGroup`.

Endpoints:

- Existing: `GET /tuition/admin/group-by-fee/list`
- Add: `POST /tuition/admin/group-by-fee/list`
- Add: `GET /tuition/admin/group-by-fee/detail/<id>`
- Add: `PUT /tuition/admin/group-by-fee/detail/<id>`
- Add: `DELETE /tuition/admin/group-by-fee/detail/<id>`

Payload fields:

- `fee`
- `price`
- `is_edit`
- `grade_level`
- `campus_id`
- `school_id`
- `program`
- `year`
- `hub_product_id`

Behavior:

- List keeps current enriched serializer with `campus`, `school`, and `grade_level`.
- Detail/create/update accepts raw IDs.
- Delete is soft delete.
- Validate `fee` exists and is not deleted.
- `price` defaults to `0` when blank.

Acceptance criteria:

- Admin can create/update/delete FeeGroup.
- FeeGroup list still returns enriched campus/school/grade data.
- Invalid or deleted Fee cannot be assigned.

## Ticket 5: UI FeeGroup Management

Add FeeGroup management UI under existing Admin Tuition area.

Recommended placement:

- Extend `/payment/admin-tuition` with tabs:
  - `Fees`
  - `Fee Groups`

FeeGroup tab behavior:

- Table columns:
  - Fee
  - Campus
  - School
  - Grade
  - Program
  - Year
  - Price
  - Editable
  - Hub Product ID
  - Actions
- Filters:
  - Fee
  - Campus
  - School
  - Grade
  - Program
  - Year
- Add/Edit dialog with selects:
  - Fee from `/tuition/admin/fee/list`
  - Campus/school/grade from existing campus endpoints
  - Program from `/tuition/student/program` or distinct FeeGroup program list
- Delete confirmation.
- Reload list after mutations.

Acceptance criteria:

- User can manage FeeGroup rows from UI.
- Filters work with existing backend list behavior.
- FeeGroup data reloads after create/update/delete.

## Ticket 6: Backend Fee Import Preview API

Add preview/validation API for Excel import.

Endpoint:

- `POST /tuition/admin/fee/import/preview`

Request:

- `multipart/form-data`
- Field: `file`
- Optional field: `sheet_name`, default `tuition_fee`

Template columns from current workbook:

- `vietnamese_name`
- `fee_name`
- `en_unit`
- `vi_unit`
- `is_compulsory`
- `is_term`
- `is_quantity`
- `fee_type`
- `due_date`
- `maturity_date`
- `enrollment_year`
- `Campus`
- `grade_level`
- `school_id`
- `program`
- `price`
- `year` from `enrollment_year`
- `is_delete`

Preview response:

- `valid_rows`
- `invalid_rows`
- `summary`

Summary fields:

- `total`
- `valid_count`
- `invalid_count`
- `create_fee_count`
- `update_fee_count`
- `create_fee_group_count`
- `update_fee_group_count`
- `delete_fee_group_count`

Each invalid row includes:

- row number
- column
- error message

Validation rules:

- Resolve FeeType by `fee_type` matching `FeeType.type`.
- Resolve/create Fee by unique `en_name` + `vi_name` intent.
- Because `Fee.en_name` and `Fee.vi_name` are separately unique, reject rows where either name conflicts with another Fee.
- FeeGroup unique key for import:
  - `fee`
  - `campus_id`
  - `school_id`
  - `grade_level`
  - `program`
  - `year`
- `price` must be numeric and `>= 0`.
- Boolean columns accept:
  - `0/1`
  - `true/false`
  - `yes/no`
- `is_delete=1` marks matching FeeGroup for deletion during commit.
- Dates parse from Excel date or `YYYY-MM-DD`.

Acceptance criteria:

- Preview returns valid/invalid rows without writing DB.
- Invalid FeeType, invalid price, missing required columns, and conflicting Fee names are reported clearly.

## Ticket 7: Backend Fee Import Commit API

Add commit API using the same validated file flow.

Endpoint:

- `POST /tuition/admin/fee/import/commit`

Request:

- `multipart/form-data`
- Field: `file`
- Optional field: `sheet_name`, default `tuition_fee`

Behavior:

- Re-run validation server-side before writing.
- If any invalid rows exist, return 400 and do not write anything.
- Use DB transaction.
- Upsert `Fee`.
- Upsert `FeeGroup`.
- Upsert `FeeDate` when `due_date`, `maturity_date`, or `enrollment_year` is present.
- FeeDate key: `fee` + `enrollment_year`.
- Soft-delete FeeGroup rows where `is_delete=1`.
- Return summary counts and row-level result.

Acceptance criteria:

- Commit creates/updates Fee, FeeGroup, and FeeDate in one transaction.
- Commit does not write if validation has any invalid rows.
- Delete rows soft-delete matching FeeGroup.

## Ticket 8: UI Import Fee/FeeGroup

Add import UI to Admin Tuition.

Recommended placement:

- Add `Import` button on `/payment/admin-tuition`.
- Open dialog using existing `ExcelPreviewDialog.vue`.

Flow:

1. User selects XLSX.
2. UI previews selected sheet.
3. User clicks `Validate`.
4. UI calls preview API.
5. UI shows:
   - summary cards
   - invalid row table
   - valid row count
6. Commit button is enabled only when `invalid_count = 0`.
7. Commit calls import commit API.
8. On success:
   - show success notification
   - close dialog
   - reload Fee and FeeGroup lists
   - refresh `tuitionStore.getOptions(true)`

Acceptance criteria:

- User can preview selected Excel sheet.
- User can validate before commit.
- Commit is blocked when invalid rows exist.
- Successful commit refreshes Fees, FeeGroups, and FeeType options.

## Backend Test Plan

- FeeType CRUD create/list/detail/update/delete.
- Fee CRUD detail endpoint works with current UI payload using `fee_type`.
- FeeGroup CRUD validates missing/deleted Fee and soft delete.
- Import preview rejects missing required columns.
- Import preview detects invalid FeeType, invalid price, and duplicate/conflicting Fee names.
- Import commit creates/updates Fee, FeeGroup, FeeDate in one transaction.
- Import commit does not write when any row is invalid.
- Import commit soft-deletes FeeGroup when `is_delete=1`.

## Frontend Check Plan

- FeeType Config page can create, edit, delete, paginate, and refresh options.
- Existing Admin Tuition Fee inline edit no longer fails due to missing backend detail endpoint.
- FeeGroup tab can create/edit/delete and filter.
- Import dialog previews workbook.
- Import dialog shows validation errors.
- Import dialog blocks commit on invalid rows.
- Import dialog commits valid file and reloads data.

## Assumptions

- Import flow is **Preview + Commit**.
- Implementation repos are:
  - `service-api` for backend
  - `ui/vue-app` for frontend
- No model migration is required for this scope.
- Admin tuition permissions can initially follow existing Tuition admin pages.
- Hardening `AllowAny` to `CustomIsAuthenticate` can be handled in the same backend tickets if desired, but must be tested against current auth flow.
- Current Excel template `Tuition/Template Import Fee.xlsx` is the source format for v1 import.
