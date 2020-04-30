

CREATE TABLE business_users(
    bu_id VARCHAR(1000) PRIMARY KEY,
    bu_address VARCHAR(20000) NOT NULL,
    bu_CName VARCHAR(36) NOT NULL,
    bu_EName VARCHAR(36), #optional (?)
    bu_picName VARCHAR(36) NOT NULL, 
    bu_phone VARCHAR(8) NOT NULL, #how about region code
    bu_isSMSVerified TINYINT(1) DEFAULT 0,
    bu_businessLogo LONGBLOB,
    bu_isDeleted TINYINT(1) DEFAULT 0,
    bu_isBusinessVerified TINYINT(1) DEFAULT 0,

    FOREIGN KEY(bu_id) REFERENCES users(ur_id)
)

CREATE TABLE individual_users(
    iu_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    iu_phone INT(8) NOT NULL, #how about region code
    iu_isSMSVerified TINYINT(1) DEFAULT 0,
    iu_profilePicture LONGBLOB,
    iu_isIndentityVerified TINYINT(1) DEFAULT 0,
    iu_CName VARCHAR(36) NOT NULL,
    iu_EName VARCHAR(36) NOT NULL,
    iu_alias VARCHAR(36) NOT NULL,
    iu_gender TINYINT(1) NOT NULL, #0 for female, 1 for male
    iu_birthday DATE NOT NULL, #YYYY-MM-DD
    iu_educationLevel TINYTEXT NOT NULL,
    iu_selfIntroduction VARCHAR(20000),
    iu_language_Cantonese TINYINT(1) NOT NULL,
    iu_language_English TINYINT(1) NOT NULL,
    iu_language_Putonghua TINYINT(1) NOT NULL,
    iu_isDeleted TINYINT(1) DEFAULT 0,
    iu_language_Other VARCHAR

    FOREIGN KEY(iu_id) REFERENCES users(ur_id)
    CONSTRAINT iu_educationLevel CHECK(
        iu_educationLevel IN ('primary school graduate','secondary school graduate', 'undergraduate or above')
)

CREATE TABLE jobs(
    jb_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    jb_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    jb_decription TEXT(20000) NOT NULL,
    jb_isDeleted TINYINT(1) DEFAULT 0,
    jb_expected_payment_days INT(36) NOT NULL

)

CREATE TABLE address(
    ads_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ads_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    ads_detail TEXT(20000) NOT NULL,

    FOREIGN KEY (ads_jb_id) REFERENCES jobs(jb_id),
    FOREIGN KEY (ads_district_id) REFERENCES districts(district_id)
)

CREATE TABLE districts(
    district_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    district_name VARCHAR(36) NOT NULL
)
CREATE TABLE abnormality(
    abn_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    abn_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    abn_type TINYTEXT() NOT NULL,
    abn_status TINYTEXT() NOT NULL,

    FOREIGN KEY (abn_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY (abn_jb_id) REFERENCES jobs(jb_id),

    CONSTRAINT abn_type_check CHECK(
        abn_type IN ('bug_report','job_abnormality', 'others')
    )
    CONSTRAINT abn_status CHECK(
        abn_status IN ('pending','processing', 'accepted','rejected', 'deleted','solved')
    )
)

CREATE TABLE job_type(
    jt_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    jt_name VARCHAR(36) NOT NULL,
    jt_description VARCHAR(20000) NOT NULL,
)

CREATE TABLE job_listings(
    li_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    li_starttime TIME NOT NULL,
    li_endtime TIME NOT NULL,
    li_salary_amt INT(20000) NOT NULL,
    li_salary_type TINYTEXT() NOT NULL,
    li_quota int(36) NOT NULL,

    FOREIGN KEY(li_jb_id) REFERENCES jobs(jb_id)
    CONSTRAINT li_salary_type CHECK(
        li_salary_type IN ('hour rate','lump sum')
)

CREATE TABLE job_applications(
    ap_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    ap_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ap_status TINYTEXT() NOT NULL,
    ap_isDeleted TINYINT(1) DEFAULT 0,
    
    FOREIGN KEY(ap_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY(ap_iu_id) REFERENCES individual_users(iu_id)

    CONSTRAINT ap_status CHECK(
        ap_status IN ('pending','offer-released','enrolled','declined by applicant','rejected by applicant','completed','reviewed')
    
)


CREATE TABLE enrollments(
    en_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    en_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    en_is_paid TINYINT(1) NOT NULL,
    en_present_status TINYTEXT() NOT NULL,
    
    FOREIGN KEY(en_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY(en_ap_id) REFERENCES job_applications(ap_id)
    
    CONSTRAINT en_present_status CHECK(
        en_present_status IN ('on time','late','absence','medical leave')

)

CREATE TABLE announcement(
    an_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    an_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    an_sender_id INT(8) NOT NULL,
    as_message TINYTEXT(20000) NOT NULL,
    as_isDeleted TINYINT(1) DEFAULT 0,

    FOREIGN KEY(an_sender_id) REFERENCES users(ur_id)
)

CREATE TABLE announcement_listings(
    PRIMARY KEY(an_id,li_id),
    FOREIGN KEY(li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY(an_id) REFERENCES job_applications(ap_id)
)

CREATE TABLE industry(
    id_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_name TINYTEXT() NOT NULL
)

CREATE TABLE users(
    ur_creationTIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    ur_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ur_login_name VARCHAR(36) NOT NULL,
    ur_password_hash INT(36) NOT NULL,
    ur_isDeleted TINYINT(1) DEFAULT 0
)

CREATE TABLE verification(
    veri_creationTIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    veri_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    veri_type TINYTEXT() NOT NULL,
    veri_doc LONGBLOB NOT NULL,
    FOREIGN KEY(veri_ur_id) REFERENCES users(ur_id),

    CONSTRAINT veri_type CHECK(
        veri_type IN ('HKID','Passport','BRC','medical doc')
)
CREATE TABLE rating_category(
    rc_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    rc_name VARCHAR() NOT NULL
    rc_rating
)

CREATE TABLE rating(
    PRIMARY KEY(ra_re_id, ra_rc_id),
    

    FOREIGN KEY(ra_re_id) REFERENCES review(re_id),
    FOREIGN KEY(ra_rc_id) REFERENCES rating_category(rc_id)
)

CREATE TABLE review(
    re_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    re_creationTIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    re_receiver_id INT(8) NOT NULL,
    re_sender_id INT(8) NOT NULL,
    re_comment TINYTEXT() NOT NULL
    re_isFollowUpNeeded TINYINT(1) NOT NULL,
    re_isDeleted TINYINT(1) DEFAULT 0,

    FOREIGN KEY(re_en_id) REFERENCES enrollments(en_id)
)

CREATE TABLE review_followup(
    rf_creationTIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    rf_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    rf_followup_time TIME NOT NULL,
    rf_comment TINYTEXT NOT NULL,

    FOREIGN KEY(rf_re_id) REFERENCES review(re_id),
    
)