CREATE TABLE business_users(
    bu_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    bu_address VARCHAR() NOT NULL,
    bu_CName VARCHAR() NOT NULL,
    bu_EName VARCHAR(), 'optional (?)
    bu_picName VARCHAR() NOT NULL, 
    bu_phone INT(8) NOT NULL, 'how about region code
    bu_isSMSVerified TINYINT(1) DEFAULT 0,
    bu_businessLogo LONGBLOB,
    bu_brc LONGBLOB,
    bu_isBusinessVerified TINYINT(1) DEFAULT 0

)

CREATE TABLE individual_users(
    iu_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    iu_phone INT(8) NOT NULL, 'how about region code
    iu_isSMSVerified TINYINT(1) DEFAULT 0,
    iu_profilePicture LONGBLOB,
    iu_hkid LONGBLOB,
    iu_passport LONGBLOB,
    iu_isIndentityVerified TINYINT(1) DEFAULT 0,
    iu_CName VARCHAR() NOT NULL,
    iu_EName VARCHAR() NOT NULL,
    iu_alias VARCHAR() NOT NULL,
    iu_gender TINYINT(1) NOT NULL, '0 for female, 1 for male
    iu_birthday DATE NOT NULL, 'YYYY-MM-DD
    iu_educationLevel TINYINT() NOT NULL,
    iu_language_Cantonese TINYINT() NOT NULL,
    iu_language_English TINYINT() NOT NULL,
    iu_language_Putonghua TINYINT() NOT NULL,
    iu_language_Other VARCHAR

)

CREATE TABLE jobs(
    jb_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    jb_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    jb_location TINYTEXT() NOT NULL,
    jb_decription TEXT() NOT NULL,
    jb_expected_payment_period TIME NOT NULL

)

CREATE TABLE job_abnormality(
    jab_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    jab_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    FOREIGN KEY (jab_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY (jab_jb_id) REFERENCES jobs(jb_id)
)

CREATE TABLE job_type(
    jt_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    jt_name VARCHAR() NOT NULL,
    jt_description VARCHAR() NOT NULL,
)

CREATE TABLE job_listings(
    li_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    li_starttime TIME NOT NULL,
    li_endtime TIME NOT NULL,
    li_salary_amt INT() NOT NULL,
    li_salary_type TINYINT() NOT NULL,
    li_quota int() NOT NULL,

    FOREIGN KEY(li_jb_id) REFERENCES jobs(jb_id)
)

CREATE TABLE job_applications(
    ap_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    ap_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ap_status TINYINT() NOT NULL,
    
    FOREIGN KEY(ap_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY(ap_iu_id) REFERENCES individual_users(iu_id)
)

CREATE TABLE enrollments(
    en_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    en_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    en_is_paid TINYINT(1) NOT NULL,
    en_is_on_time TINYINT(0),
    en_is_present TINYINT(0),
    
    FOREIGN KEY(en_li_id) REFERENCES job_listings(li_id),
    FOREIGN KEY(en_ap_id) REFERENCES job_applications(ap_id)
)

CREATE TABLE announcement(
    an_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    an_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    an_sender_id INT(8) NOT NULL,
    an_receiver_id INT(8) NOT NULL,
    as_message TINYTEXT() NOT NULL
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
    ur_login_name VARCHAR() NOT NULL,
    ur_password_hash INT() NOT NULL
)

CREATE TABLE rating_category(
    rc_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    rc_name VARCHAR() NOT NULL
)

CREATE TABLE rating(
    PRIMARY KEY(ra_re_id, ra_rc_id),

    FOREIGN KEY(ra_re_id) REFERENCES review(re_id),
    FOREIGN KEY(ra_rc_id) REFERENCES rating_category(rc_id)
)

CREATE TABLE review(
    re_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    re_type TINYINT() NOT NULL,
    re_receiver_id INT(8) NOT NULL,
    re_sender_id INT(8) NOT NULL,
    re_comment TINYTEXT() NOT NULL
    re_isFollowUpNeeded TINYINT(1) NOT NULL,

    FOREIGN KEY(re_en_id) REFERENCES enrollments(en_id)
)

CREATE TABLE review_followup(
    rf_id INT(8) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    rf_expected_time TIME NOT NULL,
    rf_comment TINYTEXT NOT NULL,

    FOREIGN KEY(rf_re_id) REFERENCES review(re_id),
    
)