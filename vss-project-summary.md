# Tom tat projects trong `C:\VSS`

Ngay quet: `2026-06-15`

## Tong quan nhanh

Trong `C:\VSS` hien co 8 thu muc co tinh chat project phat trien:

- `service-api`
- `user-management`
- `ui`
- `bff-mobile`
- `3d-gallery`
- `hrm-integrate`
- `sis-integrate`
- `sns-integrate`

Ngoai ra co mot so thu muc ha tang/ho tro, khong phai project ung dung chinh:

- `postgresql`, `redis`, `rabbitmq`: du lieu hoac local infra
- `tmp`: thu muc tam
- `docs`: tai lieu/rules/noi tong hop

## 1. `service-api`

- Loai: backend Django REST monolith
- Bang chung: `C:\VSS\service-api\src\manage.py`, `requirements.txt`, nhieu app con trong `src`
- Quy mo:
  - 24 file `models.py`
  - 190 khai bao `class` trong cac file model
  - rat nhieu domain nghiep vu trong cung mot service

### Nhiem vu chinh

`service-api` la backend nghiep vu trung tam cua he thong Victoria School. Day la service chua phan lon business logic va data model, bao gom ca nghiep vu van hanh truong hoc, thanh toan, CRM enrollment, tuition, feedback, food court, messaging, report, card, medicine, survey, post 3D.

### Cac cum domain lon doc duoc tu models va urls

- `hubspot`: enrollment CRM, hoc sinh, guardian, pipeline, consent, contract, attachment, staging sync.
  - Bang chung: `src/hubspot/models.py`, `src/hubspot/...`, endpoint `/hubspot/...`
- `payment`: order, order item, giao dich, receipt, quote, campus account, callback cong thanh toan.
  - Bang chung: `src/payment/models.py`, `src/payment/urls.py`
- `tuition`: fee, fee group, term, discount, student fee, fee type, service subscription.
  - Bang chung: `src/tuition/models.py`, `src/tuition/urls.py`
- `food`: food type, mon an, set/combo, menu theo ngay, config theo grade, register form, booking, check-in.
  - Bang chung: `src/food/models.py`
- `campus`: campus, school, grade level, class, campus info, payment info.
  - Bang chung: `src/campus/models.py`
- `authentication`: permission, role, user actor, role-permission.
  - Bang chung: `src/authentication/models.py`, `src/authentication/urls.py`
- `messaging`: email integration account, template, batch gui email/SMS, recipient tracking.
  - Bang chung: `src/messaging/models.py`, `src/messaging/urls.py`
- `feedback`: ticket tu phu huynh/hoc sinh, ly do, pipeline, follow-up, assign, approval, rating, activity log.
  - Bang chung: `src/feedback/models.py`
- `card`: card, card type, issuance, relation, service card.
  - Bang chung: `src/card/models.py`, `src/card/urls.py`
- `report`: KPI admission, tong hop doanh thu, cong no, discount, export report.
  - Bang chung: `src/report/models.py`, `src/report/urls.py`
- `report_card`: template va association report card.
- `medicine`: medicine form va attachment.
- `product`: category, brand, variant, store, cart, combo.
- `survey`: survey, question, option, participant, answer.
- `post_3d`: bai post 3D, mapping hoc sinh, tracking action cua client.

### Danh gia quy mo entity

- Day la codebase backend lon nhat trong `C:\VSS`.
- Vua la core operational API, vua la CRM/payment/tuition platform.
- Entity scale la "lon va da mien", khong phai microservice don muc tieu.

## 2. `user-management`

- Loai: backend Django cho identity va account domain
- Bang chung: `C:\VSS\user-management\user-project\manage.py`, `requirements.txt`
- Quy mo:
  - 4 file `models.py`
  - 45 khai bao `class` trong model

### Nhiem vu chinh

Day la service quan ly tai khoan va danh tinh nguoi dung, tach rieng khoi `service-api`. No phu trach login, OTP, refresh token, account profile, role, permission, application access, team, campus/department/job metadata, va lich su tich hop user.

### Entity/doc duoc tu models

- `User`, `UserType`, `Profile`, `Person`, `Address`, `Activation`, `LoginMethod`, `LoginHistory`
- `Role`, `Permission`, `RolePermission`, `UserRole`, `RoleApplication`
- `Application`, `UserApplication`
- `Campus`, `GradeLevel`, `Department`, `OrganizationTree`, `JobPosition`, `JobLevel`, `StaffCode`
- `Team`, `TeamMember`, `TeamAutomationRule`
- `UserIntegrationHistory`, `ProfileHistory`
- `EmailProcess`, `EmailTracking`, `EmailOnboarding`

### Danh gia quy mo entity

- Quy mo "vua den lon" nhung tap trung rat ro vao IAM + profile master data.
- La service rieng de `ui` dung cho auth, role, permission, account directory.

## 3. `ui`

- Loai: frontend Quasar/Vue 3
- Bang chung: `C:\VSS\ui\vue-app\package.json`
- Quy mo:
  - 476 diem goi `api`, `api_user`, `apiNoAuth`, `apiUserNoAuth` trong `src`
  - frontend nghiep vu tong hop, phu song rat nhieu module

### Cac service dang ket noi

Frontend nay chu yeu ket noi den 2 backend:

- `API_URL`
  - Bang chung: `src/boot/axios.ts`
  - Thuc te la service nghiep vu chinh, mapping toi `service-api`
- `API_USER_URL`
  - Bang chung: `src/boot/axios.ts`
  - Thuc te la service account/identity, mapping toi `user-management`

### Quy mo qua namespace endpoint

Tu `src/boot/api.ts`, `ui` dang dung endpoint thuoc cac nhom:

- `hubspot`
- `payment`
- `report`
- `tuition`
- `campus`
- `report-card`
- `hrm`
- `food`
- `bus`
- `feedback`
- `card`
- `messaging`
- `medicine`
- `authentication`
- `user`
- `address`
- `cms`

### Ket luan

- `ui` la dashboard/frontend chinh cho ca admin va client.
- No khong tu chua nghiep vu du lieu chinh, nhung quy mo giao tiep API rat lon, chung to do rong chuc nang cao.

## 4. `bff-mobile`

- Loai: backend FastAPI dang vai tro BFF cho mobile
- Bang chung: `C:\VSS\bff-mobile\src\main.py`, `requirements.txt`
- Quy mo:
  - 18 router endpoint group trong `src/routers/v1/endpoints`
  - model noi bo rat it: chu yeu `JWTPayload`, `User`

### Nhiem vu chinh

Day la lop BFF cho ung dung mobile. No khong phai he thong luu tru entity lon, ma dong vai tro adapter/orchestrator cho mobile consumption, che bien response va auth flow cho cac domain mobile.

### Domain route doc duoc

- `auth`
- `attendance`
- `assignment`
- `bus`
- `calendar`
- `course`
- `feedback`
- `food`
- `guardian`
- `home-room`
- `medicine`
- `media`
- `payment`
- `post`
- `report`
- `staff`
- `tuition`

### Danh gia quy mo entity

- Entity local nho
- Router surface lon
- Ban chat la integration/orchestration layer cho mobile, khong phai master-data backend

## 5. `3d-gallery`

- Loai: frontend Nuxt 4 + Three.js/TresJS
- Bang chung: `C:\VSS\3d-gallery\nuxt-app\package.json`, `nuxt.config.ts`
- Quy mo service connection:
  - runtime config co `crmApi`
  - logic API tap trung quanh `post-3d`

### Cac service dang ket noi

- `crmApi`
  - Bang chung: `nuxt.config.ts`, `app/composables/usePost3D.ts`
  - Goi cac endpoint:
    - `/post-3d/detail/{id}`
    - `/post-3d/client/{slug}`
    - `/post-3d/client/{slug}/stats`

### Ket luan

- Frontend nay co muc tieu hep va ro: hien thi/tuong tac gallery 3D.
- Quy mo backend dependency nho, chu yeu dua vao `service-api` module `post_3d` thong qua `crmApi`.

## 6. `hrm-integrate`

- Loai: backend Django integration service
- Bang chung: `C:\VSS\hrm-integrate\hrm-project\manage.py`, `requirements.txt`
- Quy mo:
  - 3 file `models.py`
  - 13 khai bao `class` trong model

### Nhiem vu chinh

Day la service dong bo va xu ly du lieu nhan su/attendance tu he thong HRM va gate device vao he sinh thai noi bo.

### Entity/doc duoc

- `MisaStaff`: mapping nhan su MISA sang ma nguoi Victoria School
- `MisaStaffDuplicate`: luu truong hop duplicate can xu ly
- `MisaStaffLog`: log payload/response dong bo
- `OrganizationUnit`, `JobPosition`, `StaffStatus`, `Campus`
- `AttendanceRecord`: log quet vao/ra, card, source device

### Endpoint nhiem vu doc duoc

- `/gate/sync-attendance`
- `/gate/attendance/by/person-number/...`
- `/gate/person-info`
- nhom `hrm/` va `gate/`

### Danh gia quy mo entity

- Quy mo entity vua phai
- Focus rat ro vao HR sync + attendance ingestion

## 7. `sis-integrate`

- Loai: backend Django integration service
- Bang chung: `C:\VSS\sis-integrate\src\manage.py`, `requirements.txt`
- Quy mo:
  - 3 file `models.py`
  - 8 khai bao `class` trong model

### Nhiem vu chinh

Day la service trung gian dong bo du lieu SIS/PowerSchool vao he thong noi bo, dac biet la campus, school, homeroom, term va mapping hoc sinh.

### Entity/doc duoc

- `Campus`, `School`, `GradeLevel`, `HomeRoom`, `Term`
- `StudentMapping`: map `student_dcid` va `student_number`
- `EnrollmentStudentLog`: log dong bo enrollment

### Endpoint nhiem vu doc duoc

- `/campus/list`
- `/campus/school/list`
- `/campus/homeroom/list/{school_id}`
- `/campus/term-info/list`
- `/campus/internal/homeroom/sync-signal`
- `/ps/...`

### Danh gia quy mo entity

- Quy mo entity nho den vua
- Muc tieu chinh la master-data sync tu SIS, khong phai ung dung business end-user

## 8. `sns-integrate`

- Loai: backend FastAPI notification service
- Bang chung: `C:\VSS\sns-integrate\src\main.py`, `requirements.txt`
- Quy mo:
  - 6 khai bao `class` trong `src/models`
  - router rieng cho `email`, `sms`, `media`, `notify`, `health`

### Nhiem vu chinh

Day la service gui va quan ly kenh thong bao, tach rieng khoi business API.

### Entity/doc duoc

- `Emails`, `EmailUnsubscribed`
- `Sms`, `SmsUnsubscribed`
- `BaseModel`, `Base`

### Endpoint nhiem vu doc duoc

- `/api/emails/list`
- `/api/emails/detail/{id}`
- `/api/emails/create`
- `/api/emails/unsubscribed-email`
- `/api/sms/list`
- `/api/sms/bulk-create`

### Danh gia quy mo entity

- Entity domain nho
- Chuc nang service ro rang: queue/luu/giam sat gui email SMS, unsubscribe, media support

## Kien truc tong the dang hien ra

- `service-api` la backend business core lon nhat
- `user-management` la identity/account service rieng
- `ui` la frontend admin/client chinh, goi ca `service-api` va `user-management`
- `bff-mobile` la lop BFF danh cho mobile
- `3d-gallery` la frontend nho, chuyen cho module `post-3d`
- `hrm-integrate`, `sis-integrate`, `sns-integrate` la cac integration/support service chuyen biet

## File tham chieu chinh da quet

- `C:\VSS\service-api\src\*\models.py`
- `C:\VSS\service-api\src\*\urls.py`
- `C:\VSS\user-management\user-project\user\models.py`
- `C:\VSS\user-management\user-project\user\urls.py`
- `C:\VSS\ui\vue-app\src\boot\axios.ts`
- `C:\VSS\ui\vue-app\src\boot\api.ts`
- `C:\VSS\bff-mobile\src\main.py`
- `C:\VSS\bff-mobile\src\routers\v1\endpoints\*.py`
- `C:\VSS\3d-gallery\nuxt-app\app\composables\usePost3D.ts`
- `C:\VSS\3d-gallery\nuxt-app\nuxt.config.ts`
- `C:\VSS\hrm-integrate\hrm-project\hrm\models.py`
- `C:\VSS\hrm-integrate\hrm-project\gate\models.py`
- `C:\VSS\sis-integrate\src\campus\models.py`
- `C:\VSS\sis-integrate\src\ps\models.py`
- `C:\VSS\sns-integrate\src\models\*.py`
- `C:\VSS\sns-integrate\src\routers\*.py`
