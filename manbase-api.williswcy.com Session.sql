SET foreign_key_checks = 0;
-- Drop tables
drop table if exists users, business_users, individual_users, jobs, job_listings, business_address, districts, abormality, job_type, job_applications, enrollments, announcement, announcement_listingsk, industry, rating_category, rating, review, review_followup;
SET foreign_key_checks = 1;

DROP TABLE job_listings;

CREATE TABLE users(
    ur_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    ur_id VARCHAR(1000) PRIMARY KEY,
    ur_login VARCHAR(36) NOT NULL,
    ur_password_hash INT(36) NOT NULL,
    ur_isDeleted TINYINT(1) DEFAULT 0
)


CREATE TABLE business_users(
    bu_id VARCHAR(1000) PRIMARY KEY,
    bu_address VARCHAR(20000) NOT NULL,
    bu_CName VARCHAR(36) NOT NULL,
    bu_EName VARCHAR(36), #optional
    bu_picName VARCHAR(36) NOT NULL, 
    bu_phone VARCHAR(8) NOT NULL, 
    bu_isSMSVerified TINYINT(1) DEFAULT 0,
    bu_businessLogo LONGBLOB,
    bu_isDeleted TINYINT(1) DEFAULT 0,
    bu_BusinessVerificationStatus TINYTEXT DEFAULT 'not verified',

    FOREIGN KEY(bu_id) REFERENCES users(ur_id)
    CONSTRAINT bu_BusinessVerificationStatus CHECK
    (bu_BusinessVerificationStatus IN ('not verified','pending', 'verified'))
)

CREATE TABLE individual_users(
    iu_id VARCHAR(1000) PRIMARY KEY,
    iu_phone INT(8) NOT NULL, #how about region code
    iu_isSMSVerified TINYINT(1) DEFAULT 0,
    iu_profilePicture LONGBLOB,
    iu_isIndentityVerified TINYINT(1) DEFAULT 0,
    iu_CName VARCHAR(36) NOT NULL,
    iu_EName VARCHAR(36) NOT NULL,
    iu_alias VARCHAR(36) NOT NULL,
    iu_HKID_head VARCHAR(1) NOT NULL,
    iu_HKID_tail VARCHAR(3) NOT NULL,
    iu_gender TINYINT(1) NOT NULL, #0 for female, 1 for male, 2 for others
    iu_birthday DATE NOT NULL, #YYYY-MM-DD
    iu_educationLevel TINYTEXT NOT NULL,
    iu_selfIntroduction VARCHAR(20000),
    iu_language_Cantonese TINYINT(1) NOT NULL,
    iu_language_English TINYINT(1) NOT NULL,
    iu_language_Putonghua TINYINT(1) NOT NULL,
    iu_isDeleted TINYINT(1) DEFAULT 0,
    iu_language_Other VARCHAR(36),

    FOREIGN KEY(iu_id) REFERENCES users(ur_id),
    CONSTRAINT iu_educationLevel CHECK
        (iu_educationLevel IN ('primary school graduate','secondary school graduate', 'undergraduate or above'))

)

CREATE TABLE jobs(
    jb_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    jb_id VARCHAR(1000) PRIMARY KEY,
    jb_decription TEXT(20000) NOT NULL,
    jb_isDeleted TINYINT(1) DEFAULT 0,
    jb_expected_payment_days INT(36) NOT NULL
)

CREATE TABLE job_listings(
    li_id VARCHAR(1000) PRIMARY KEY,
    li_jb_id VARCHAR(1000) NOT NULL,
    li_starttime TIME NOT NULL,
    li_endtime TIME NOT NULL,
    li_salary_amt INT(255) NOT NULL,
    li_salary_type TINYTEXT NOT NULL,
    li_quota INT(36) NOT NULL,

    FOREIGN KEY(li_jb_id) REFERENCES jobs(jb_id),
    CONSTRAINT li_salary_type CHECK(
        li_salary_type IN ('hour rate','lump sum'))
)

CREATE TABLE business_address(
    bads_id VARCHAR(1000) PRIMARY KEY,
    bads_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    bads_detail TEXT(20000) NOT NULL,
    bads_jb_id VARCHAR(1000) NOT NULL,
    bads_district_id VARCHAR(1000) NOT NULL,

    FOREIGN KEY (bads_jb_id) REFERENCES jobs(jb_id),
    FOREIGN KEY (bads_district_id) REFERENCES districts(district_id)
)

CREATE TABLE districts(
    district_id VARCHAR(1000) PRIMARY KEY,
    district_name VARCHAR(36) NOT NULL
)

CREATE TABLE abnormality(
    abn_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    abn_id VARCHAR(1000) PRIMARY KEY,
    abn_type TINYTEXT NOT NULL,
    abn_status TINYTEXT NOT NULL,
    abn_jb_id VARCHAR(1000) NOT NULL,
    abn_li_id VARCHAR(1000) NOT NULL,

    FOREIGN KEY (abn_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY (abn_jb_id) REFERENCES jobs(jb_id),

    CONSTRAINT abn_type_check CHECK(
        abn_type IN ('bug_report','job_abnormality', 'others')),

    CONSTRAINT abn_status CHECK(
        abn_status IN ('pending','processing', 'accepted','rejected', 'deleted','solved'))
)

CREATE TABLE job_type(
    jt_id VARCHAR(1000) PRIMARY KEY,
    jt_name VARCHAR(36) NOT NULL,
    jt_description VARCHAR(20000) NOT NULL
)


CREATE TABLE job_applications(
    ap_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    ap_id VARCHAR(1000) PRIMARY KEY,
    ap_status TINYTEXT NOT NULL,
    ap_isDeleted TINYINT(1) DEFAULT 0,
    ap_li_id VARCHAR(1000) NOT NULL,
    ap_iu_id VARCHAR(1000) NOT NULL,
    
    FOREIGN KEY(ap_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY(ap_iu_id) REFERENCES individual_users(iu_id),

    CONSTRAINT ap_status CHECK(
        ap_status IN ('pending','offer-released','enrolled','declined by applicant','rejected by applicant','completed','reviewed')
        )
)


CREATE TABLE enrollments(
    en_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    en_id VARCHAR(1000) PRIMARY KEY,
    en_is_paid TINYINT(1) NOT NULL,
    en_present_status TINYTEXT NOT NULL,
    en_li_id VARCHAR(1000) NOT NULL,
    en_ap_id VARCHAR(1000) NOT NULL,
    
    FOREIGN KEY(en_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY(en_ap_id) REFERENCES job_applications(ap_id),
    
    CONSTRAINT en_present_status CHECK(
        en_present_status IN ('on time','late','absence','medical leave')
        )
)

CREATE TABLE announcement(
    an_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    an_id VARCHAR(1000) PRIMARY KEY,
    an_message TEXT(20000) NOT NULL,
    an_isDeleted TINYINT(1) DEFAULT 0,
    an_sender_id VARCHAR(1000) NOT NULL,

    FOREIGN KEY(an_sender_id) REFERENCES users(ur_id)
)

CREATE TABLE announcement_listings(
    anli_an_id VARCHAR(1000) NOT NULL,
    anli_li_id VARCHAR(1000) NOT NULL,
    PRIMARY KEY(anli_an_id,anli_li_id),
    anli_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY(anli_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY(anli_an_id) REFERENCES job_applications(ap_id)
)

CREATE TABLE industry(
    ind_id VARCHAR(1000) PRIMARY KEY,
    ind_name TEXT(36) NOT NULL
)

CREATE TABLE verification(
    veri_creationTIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    veri_id VARCHAR(1000) PRIMARY KEY,
    veri_type TINYTEXT NOT NULL,
    veri_doc LONGBLOB NOT NULL,
    veri_ur_id VARCHAR(1000) NOT NULL,

    FOREIGN KEY(veri_ur_id) REFERENCES users(ur_id),

    CONSTRAINT veri_type CHECK(
        veri_type IN ('HKID','Passport','BRC','medical doc')
        )
)

CREATE TABLE rating_category(
    rc_id VARCHAR(1000) PRIMARY KEY,
    rc_name VARCHAR(36) NOT NULL
)

CREATE TABLE rating(
    rate_re_id VARCHAR(1000) NOT NULL,
    rate_rc_id VARCHAR(1000) NOT NULL,
    PRIMARY KEY(rate_re_id, rate_rc_id),
    rate_score INT(5) NOT NULL,

    FOREIGN KEY(rate_re_id) REFERENCES review(re_id),
    FOREIGN KEY(rate_rc_id) REFERENCES rating_category(rc_id)
)

CREATE TABLE review(
    re_id VARCHAR(1000) PRIMARY KEY,
    re_creationTIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    re_receiver_id INT(8) NOT NULL,
    re_sender_id INT(8) NOT NULL,
    re_comment TEXT(20000) NOT NULL,
    re_isFollowUpNeeded TINYINT(1) NOT NULL,
    re_isDeleted TINYINT(1) DEFAULT 0,
    re_en_id VARCHAR(1000) NOT NULL,

    FOREIGN KEY(re_en_id) REFERENCES enrollments(en_id)
)

CREATE TABLE review_followup(
    rf_creationTIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    rf_id VARCHAR(1000) PRIMARY KEY,
    rf_followup_time TIME NOT NULL,
    rf_comment TEXT(30000) NOT NULL,
    rf_re_id VARCHAR(1000) NOT NULL,

    FOREIGN KEY(rf_re_id) REFERENCES review(re_id)
)