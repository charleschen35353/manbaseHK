```plantuml
@startuml
    class business_users {
        - bu_id
        - bu_address
        - bu_CName
        - bu_EName
            'english and chinese name
        - bu_phone
        - bu_isSMSVerified
        - bu_businessLogo
        - bu_brc
            'business registration certification
        - bu_isBusinessVerified
            'verification: True or False
        - bu_isDeleted

'function
        - createBusinessProfile()
            'register business user
        - viewBusinessProfile()
        - updateBusinessProfile()
        - deleteBusinessProfile()
        - updateBusinessPhone()
        - viewJobApplicant()
            'view job applicant: personal info., rating stat, comment,
        - viewPassedJob()
        - approveJobApplication()
            'send job offer
        - declineJobApplication()

        - rateIndividual()

        - changePhone()
        - changePIC()

    }

    class individual_users {
    'attributes
        - iu_id
        - iu_phone
        - iu_isSMSVerified
            'for SMS verification
        - iu_profilePicture
            'profile picture [opt]
        - iu_hkid
        - iu_passport
            'for real identity verification [opt]
        - iu_isIdentityVerified
            'real identity verification: True or False
        - iu_CName
        - iu_EName
        - iu_alias
            'one name
        - iu_gender
        - iu_birthday
        - iu_educationLevel
            'primary secondary school, tertiary...
        - iu_selfIntroduction
            'string data, may be have identity disclosure isuue (?) [opt]
        - iu_language_Cantonese
        - iu_language_English
        - iu_language_Putonghua
            'capable work lanuage: ture or false
        - iu_language_Other
            'user specified language: str [opt]
        - iu_isDeleted

    'functions
        - uploadMyProfilePicture()
        - viewMyProfilePicture()
        - deleteMyProfilePicture()
            'profile pic
        - createMyIndividualProfile()
            'register
        - viewMyProfile()
        - updateMyProfile()
            'for non compulsary attributes
        - deleteIndividualProfile()
            'individual account
        - identityVerification()
            'submit hkid/passport
        - changePassword()
        '- updateIdentityVerificationStatus()
            'not sure if put here (?)
        '- updateSMSVerificationStatus()
            'not sure if need put
        - showIndividualReview()
        - updateIndividualPhone()

        - viewJobBoard()
        - viewJobBoard_salary()
        - viewJobBoard_rating()
        - viewJobBoard_distance()

        - acceptJobOffer()
        - declineJobOffer()

        - rateBusiness()
        
        - changePhone()
        '- changeBitrhday()
            'once

    }

    class jobs {
    'attributes
        - jb_id
        '- jb_type
            'added a new job_type class
        - jb_location
            'district class, area class, + string
        - jb_creationTime
        - jb_description
            'collapsed with job type description(?)
        - jb_expected_payment_days
            'number, in days
        - jb_isDeleted

    'functions
        - createJob()
        - viewJob()
            'view specific job detail (?) or job board
        - updateJob()
            'edit job
        - deleteJob()
            'cancel job for business user

        - displayByType()
        - displayBySalary()
        - displayByLocation()
            'filter function for job board
        - showPostedJob()
            'business
        
        
    }

    class abnormality{
    'attribute
        - abn_creationTime
        - abn_id
        - abn_type
        - abn_li_id
            'can be null
            '[opt]
        - abn_job_id
            '[opt]
        - abn_sender
            'store user id
        - abn_description
        - abn_status
            'pending, processing, accepted, rejected, deleted, solved

    'function
        - reportAbnormality()
            'create
        - view()
       '- update() : should be banned(?)
        - delete()

        - solve()
            'change jab_isSolved to True

    }

    class job_type {
    'attirbutes
        - jt_id
        - jt_name

    'functions
        - create()
        - view()
        - update()
        - Delete()
    }

    class job_listings {
    'attributes
        - li_id
        - li_jb_id
        - li_starttime
        - li_endtime
        - li_salary_amt
            ' in number
        - li_salary_type
            ' salary structure: in hr rate or lump sum
        - li_ot_salary
            ' number, in hour rate
        - li_quota
            ' the amount for workforce needed

        'functions
        - create()
        - update()
        - view()
            'view listing detail
        - delete()
            'cancel job post: not allowed when more than one enrolled individual
    }

    class job_applications {
    'attribute
        - ap_creationTime
            'application time for waitlist
        - ap_id
        - ap_li_id
            'listed job
        - ap_iu_id
            'applicant
        - ap_status
            'enrollment status, can be waitlist
        - ap_isDeleted

    'function
        - create()
            'apply for job
        - delete()
            'withdraw job application
        - update()
            'for admin
        - view()
            'view my job for individual/ view applicants (?)

        - accept()
            'change of status from approved to accepted by individual


        }

    'class waitlist {
        '- wl_id
       ' - wl_ap_id
        '- wl_iu_id
        '- wl_time
            'decide waitlist position

    '}

    class enrollments {
    'attribute
        - en_creationTime
            'enrollment time
        - en_id
        - en_ap_id
        - en_li_id
        - en_is_paid
        - en_present_status
            'on_time, late, absence, medical_leave (supporting doc)
        
    'function
        - create()
        - update()
        - view()
        - delete()

        - viewEmployee()
            'view enrolled individual for a specific job
        - confirmAttendance()
            'change attendance status of individual, by employer
        -
    }

    class announcement {
    'canvas discussion board

    'attribute
        - an_creationTime
        - an_id
        - an_sender_id
        - an_message
        - an_isDeleted

    'function
        - create()
            'release a message
        - 'update()
            'not allowed (?)
        - view()
            'business or individual
        - delete()
            'not allowed after certain time


    }

    class announcement_listings {
        - an_id
        - li_id
    }

    class industry {
    'attribute
        - id_id
        - id_name
    'function
        - create()
        - update()
        - view()
        - delete()
    }

    class users {
        - ur_creationTime
        - ur_id
        - ur_login_name
        - ur_password_hash
        - ur_isDeleted

    'function
        - create()
        - updatePassword()
        - delete()
    }

    class rating_category {
    'attrbute
        - rc_id
        - rc_name
            '1-5 scale
            'individual performance
    'function
        - create()
        - view()
        - update()
        - delete()
    }

    class rating {
    'attribute
        - ra_re_id
        - ra_rc_id
        - ra_rating
            'Workload, Work Environment, Administration: 1-5 scale
            'individual performance: -2, -1, 0, 1, 2 scale

    'function
        - createRating()
        - viewRating()
        - updateRating()
            'for admin
        - deleteRating()
            'for admin

        - getAverageRating()
            'display on individual profile / job application
    }

    class review {
    'attribute
        - re_creationTime
        - re_id
        - re_en_id
        - re_receiver_id
        - re_sender_id
        - re_comment
        - re_isFollowUpNeeded
            'for the payment day later than review day: True or False, 追加comment
        - re_isDeleted

    'function
        - viewReview()
            'view comment
        - createReview()
        - updateReview()
            'for admin(?), how about 追數 (?)
        - deleteReview()
            'for admin(?)

    }

    class review_followup{
    'attribute
        - rf_creationTime
        - rf_id
        - rf_re_id
        - rf_followup_time
            'the expected day of salary payment
        - rf_comment

    'function
        - viewFollowUp()
        - createFollowUp()
        - updateFollowUp()
            'make follow-up review
        - deleteFollowUp()
            'for admin

    }

    users "1..1" -- "0..M" announcement: create

    announcement "1..1" -- "0..M" announcement: reply

    users "1..1" -- "1..M" individual_users: is

    users "1..1" -- "1..M" business_users: is

    industry "1..1" -- "0..M" business_users: in_industry

    business_users "1..1" -- "1..M" jobs

    job_listings "1..1" - "0..M" job_applications: apply

    jobs "1..1" -- "1..M" job_listings

    jobs "0..M" -- "1..1" job_type

    jobs "1..1" -- "0..M" job_abnormality

    job_applications "0..M" -up- "1..1" individual_users

    job_listings "1..1" -- "0..M" enrollments

    job_listings "0..1" -- "0..M" job_abnormality

    job_applications "1..1" -- "0..M" enrollments

    announcement "1..1" -- "1..M" announcement_listings

    announcement_listings "0..M" -- "1..1" job_listings

    enrollments "1..1" -- "0..M" review

    review "1..1" -left- "1..M" rating

    review "0..M" -- "1..1" users

    review "1..1" -- "0..1" review_followup

    rating "1..1" -- "0..M" rating_category
@enduml
```
