SET foreign_key_checks = 0;
-- Drop tables
drop table if exists users, districts, job_type, industry, business_users, individual_users, jobs, job_listings, business_address, abnormality, job_applications, enrollments, announcement, announcement_listings, verification, rating_category, review, rating, review_followup,job_nature;
SET foreign_key_checks = 1;

CREATE TABLE users(
    ur_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    ur_id VARCHAR(255) PRIMARY KEY,
    ur_login VARCHAR(36) NOT NULL,
    ur_password_hash VARCHAR(255) NOT NULL,
    ur_isDeleted TINYINT(1) DEFAULT 0,
    ur_phone VARCHAR(8) NOT NULL, 
    ur_email VARCHAR(255) NOT NULL,
    ur_email_key VARCHAR(255),
    ur_sms_key VARCHAR(255),
    ur_reset_key VARCHAR(255),
    ur_isSMSVerified TINYINT(1) DEFAULT 0,
    ur_isEmailVerified TINYINT(1) DEFAULT 0,
    ur_otp_hash VARCHAR(255)
) CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE districts(
    district_id VARCHAR(255) PRIMARY KEY,
    district_name VARCHAR(36) NOT NULL
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE job_type(
    jt_id VARCHAR(255) PRIMARY KEY,
    jt_name VARCHAR(36) NOT NULL,
    jt_description VARCHAR(20000) NOT NULL,
    jt_isApproved BOOLEAN NOT NULL
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE industry(
    ind_id VARCHAR(255) PRIMARY KEY,
    ind_name TEXT(36) NOT NULL
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE business_users(
    bu_id VARCHAR(255) PRIMARY KEY,
    bu_ind_id VARCHAR(255),
    bu_CName VARCHAR(36) NOT NULL,
    bu_EName VARCHAR(36), #optional
    bu_picName VARCHAR(36) NOT NULL, 
    bu_confirmation_sent_on TIMESTAMP,
    bu_businessLogo VARCHAR(255),
    bu_isDeleted TINYINT(1) DEFAULT 0,
    bu_BusinessVerificationStatus VARCHAR(1) DEFAULT 0, #0 is not verified, 1 is pending, 2 is verified

    FOREIGN KEY(bu_id) REFERENCES users(ur_id),
    FOREIGN KEY(bu_ind_id) REFERENCES industry(ind_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE business_address(
    bads_id VARCHAR(255) PRIMARY KEY,
    bads_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    bads_detail TEXT(20000) NOT NULL,
    bads_bu_id VARCHAR(255) NOT NULL,
    bads_district_id VARCHAR(255) NOT NULL,
    bads_isMajorAddress BOOLEAN NOT NULL,

    FOREIGN KEY (bads_bu_id) REFERENCES business_users(bu_id),
    FOREIGN KEY (bads_district_id) REFERENCES districts(district_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE individual_users(
    iu_id VARCHAR(255) PRIMARY KEY,
    iu_profilePicture VARCHAR(2048),
    iu_confirmation_sent_on TIMESTAMP,
    iu_CName VARCHAR(36) NOT NULL,
    iu_EName VARCHAR(36) NOT NULL,
    iu_alias VARCHAR(36) NOT NULL,
    iu_HKID VARCHAR(9) NOT NULL,
    iu_gender TINYINT(1) NOT NULL, #0 for female, 1 for male, 2 for others
    iu_birthday DATE NOT NULL, #YYYY-MM-DD
    iu_educationLevel TINYTEXT NOT NULL,
    iu_selfIntroduction TEXT(20000),
    iu_language_Cantonese TINYINT(1) NOT NULL,
    iu_language_English TINYINT(1) NOT NULL,
    iu_language_Putonghua TINYINT(1) NOT NULL,
    iu_isDeleted TINYINT(1) DEFAULT 0,
    iu_language_Other VARCHAR(36),

    FOREIGN KEY(iu_id) REFERENCES users(ur_id),
    CONSTRAINT iu_educationLevel CHECK
        (iu_educationLevel IN ('primary school graduate','secondary school graduate', 'undergraduate or above'))
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE job_nature(
    jbna_id VARCHAR(255) PRIMARY KEY,
    jbna_name VARCHAR(255) NOT NULL,
    jbna_description VARCHAR(255)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE jobs(
    jb_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    jb_id VARCHAR(255) PRIMARY KEY,
    jb_title VARCHAR(255) NOT NULL,
    jb_description TEXT(20000) NOT NULL,
    jb_isDeleted TINYINT(1) DEFAULT 0,
    jb_expected_payment_days INT(36) NOT NULL,
    jb_bu_id VARCHAR(255) NOT NULL,
    jb_jt_id VARCHAR(255) NOT NULL,
    jb_bads_id VARCHAR(255) NOT NULL,
    jb_ind_id VARCHAR(255) NOT NULL,
    jb_jbna_id VARCHAR(255) NOT NULL,

    FOREIGN KEY(jb_jt_id) REFERENCES job_type(jt_id),
    FOREIGN KEY (jb_bu_id) REFERENCES business_users(bu_id),
    FOREIGN KEY (jb_bads_id) REFERENCES business_address(bads_id),
    FOREIGN KEY(jb_ind_id) REFERENCES industry(ind_id),
    FOREIGN KEY(jb_jbna_id) REFERENCES job_nature(jbna_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE job_listings(
    li_id VARCHAR(255) PRIMARY KEY,
    li_jb_id VARCHAR(255) NOT NULL,
    li_salary_amt INT(255) NOT NULL,
	li_endtime TIMESTAMP DEFAULT current_timestamp,
    li_starttime DATETIME DEFAULT current_timestamp,
    li_salary_type TINYTEXT NOT NULL,
    li_quota INT(36) NOT NULL,

    FOREIGN KEY(li_jb_id) REFERENCES jobs(jb_id),
    CONSTRAINT li_salary_type CHECK(
        li_salary_type IN ('hour rate','lump sum'))
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE abnormality(
    abn_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    abn_id VARCHAR(255) PRIMARY KEY,
    abn_type TINYTEXT NOT NULL,
    abn_status TINYTEXT NOT NULL,
    abn_jb_id VARCHAR(255) NOT NULL,
    abn_li_id VARCHAR(255),
    abn_message VARCHAR(255) NOT NULL,
    abn_ur_id VARCHAR(255) NOT NULL,

    FOREIGN KEY (abn_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY (abn_jb_id) REFERENCES jobs(jb_id),
    FOREIGN KEY (abn_ur_id) REFERENCES users(ur_id),

    CONSTRAINT abn_type_check CHECK(
        abn_type IN ('bug_report','job_abnormality', 'others')),

    CONSTRAINT abn_status CHECK(
        abn_status IN ('pending','processing', 'accepted','rejected', 'deleted','solved'))
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE job_applications(
    ap_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    ap_id VARCHAR(255) PRIMARY KEY,
    ap_status TINYTEXT NOT NULL,
    ap_isDeleted TINYINT(1) DEFAULT 0,
    ap_li_id VARCHAR(255) NOT NULL,
    ap_iu_id VARCHAR(255) NOT NULL,
    
    FOREIGN KEY(ap_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY(ap_iu_id) REFERENCES individual_users(iu_id),

    CONSTRAINT ap_status CHECK(
        ap_status IN ('pending','offer-released','enrolled','declined by applicant','rejected by applicant','completed','reviewed')
        )
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;


CREATE TABLE enrollments(
    en_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    en_id VARCHAR(255) PRIMARY KEY,
    en_is_paid TINYINT(1),
    en_present_status TINYTEXT,
    en_li_id VARCHAR(255) NOT NULL,
    en_ap_id VARCHAR(255) NOT NULL,
    
    FOREIGN KEY(en_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY(en_ap_id) REFERENCES job_applications(ap_id),
    
    CONSTRAINT en_present_status CHECK(
        en_present_status IN ('on time','late','absence','medical leave')
        )
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE announcement(
    an_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    an_id VARCHAR(255) PRIMARY KEY,
    an_message TEXT(255) NOT NULL,
    an_isDeleted TINYINT(1) DEFAULT 0,
    an_sender_id VARCHAR(255) NOT NULL,
    an_isFromEmployer TINYINT(1) DEFAULT 0 NOT NULL,
    an_replyTo VARCHAR(255),

    FOREIGN KEY(an_sender_id) REFERENCES users(ur_id),
    FOREIGN KEY(an_replyTo) REFERENCES announcement(an_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE announcement_listings(
    anli_an_id VARCHAR(255) NOT NULL,
    anli_li_id VARCHAR(255) NOT NULL,
    PRIMARY KEY(anli_an_id,anli_li_id),
    anli_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY(anli_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY(anli_an_id) REFERENCES announcement(an_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE verification(
    veri_creationTIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    veri_id VARCHAR(255) PRIMARY KEY,
    veri_type TINYTEXT NOT NULL,
    veri_doc VARCHAR(2048) NOT NULL,
    veri_ur_id VARCHAR(255) NOT NULL,
    veri_isApproved TINYINT(1) DEFAULT 0,

    FOREIGN KEY(veri_ur_id) REFERENCES users(ur_id),

    CONSTRAINT veri_type CHECK(
        veri_type IN ('HKID','Passport','BRC','medical doc')
        )
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE rating_category(
    rc_id VARCHAR(255) PRIMARY KEY,
    rc_name VARCHAR(36) NOT NULL
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE review(
    re_id VARCHAR(255) PRIMARY KEY,
    re_creationTIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    re_receiver_id VARCHAR(255) NOT NULL,
    re_sender_id VARCHAR(255) NOT NULL,
    re_comment TEXT(20000) NOT NULL,
    re_isDeleted TINYINT(1) DEFAULT 0,
    re_en_id VARCHAR(255) NOT NULL,

    FOREIGN KEY(re_en_id) REFERENCES enrollments(en_id),
    FOREIGN KEY(re_receiver_id) REFERENCES users(ur_id),
    FOREIGN KEY(re_sender_id) REFERENCES users(ur_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE rating(
    rate_re_id VARCHAR(255) NOT NULL,
    rate_rc_id VARCHAR(255) NOT NULL,
    PRIMARY KEY(rate_re_id, rate_rc_id),
    rate_score INT(5) NOT NULL,

    FOREIGN KEY(rate_re_id) REFERENCES review(re_id),
    FOREIGN KEY(rate_rc_id) REFERENCES rating_category(rc_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE review_followup(
    rf_creationTIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    rf_id VARCHAR(255) PRIMARY KEY,
    rf_followup_time TIME NOT NULL,
    rf_comment TEXT(20000) NOT NULL,
    rf_re_id VARCHAR(255) NOT NULL,

    FOREIGN KEY(rf_re_id) REFERENCES review(re_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;