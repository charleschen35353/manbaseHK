use manbasedb_new;

SET foreign_key_checks = 0;
-- Drop tables
drop table if exists users, freelancers, employers, jobs, job_qna, job_sessions, job_addresses, job_applications, external_transactions, chatrooms, chatroom_participants, messages, tags, clock_in_out, exit_surveys, rating_categories, ratings, comments,comment_categories, internal_transactions, reports, job_types;
SET foreign_key_checks = 1;

CREATE TABLE users(
    ur_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    ur_id VARCHAR(255) PRIMARY KEY,
    ur_login VARCHAR(36) NOT NULL,
    ur_password_hash VARCHAR(255) NOT NULL,
    ur_phone VARCHAR(8) NOT NULL, 
	ur_email VARCHAR(255) NOT NULL,
    ur_type TINYINT(1) NOT NULL,
    ur_isDeleted TINYINT(1) DEFAULT 0,
    ur_sms_key VARCHAR(255),
    ur_email_key VARCHAR(255),
    ur_reset_key VARCHAR(255),
    ur_isSMSVerified TINYINT(1) DEFAULT 0,
    ur_isEmailVerified TINYINT(1) DEFAULT 0,
    ur_otp_hash VARCHAR(255)
) CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE freelancers(
    fl_id VARCHAR(255) PRIMARY KEY,
	fl_CName VARCHAR(36) NOT NULL,
    fl_EName VARCHAR(36) NOT NULL,
	fl_alias VARCHAR(36) NOT NULL,
	fl_educationLevel TINYTEXT NOT NULL,
    fl_birthday DATE NOT NULL, #YYYY-MM-DD
    fl_gender TINYINT(1) NOT NULL, #0 for female, 1 for male, 2 for others
    fl_residentialDistrict TINYINT(2) NOT NULL,
    fl_residentialAddress TEXT(200),
    fl_profilePicture VARCHAR(2048),
    fl_confirmation_sent_on TIMESTAMP,
    #fl_selfIntroduction TEXT(20000), not sure
    #fl_language_Cantonese TINYINT(1) NOT NULL,
    #fl_language_English TINYINT(1) NOT NULL,
    #fl_language_Putonghua TINYINT(1) NOT NULL,
    fl_isDeleted TINYINT(1) DEFAULT 0,
    #fl_language_Other VARCHAR(36),

    FOREIGN KEY(fl_id) REFERENCES users(ur_id)
    #CONSTRAINT fl_educationLevel CHECK
        #(fl_educationLevel IN ('primary school graduate','secondary school graduate', 'undergraduate or above'))
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE employers(
    em_id VARCHAR(255) PRIMARY KEY,
    em_companyName VARCHAR(36), #optional
    em_picName VARCHAR(36) NOT NULL, 
    em_confirmation_sent_on TIMESTAMP,
    em_profilePicture VARCHAR(255),
    em_isDeleted TINYINT(1) DEFAULT 0,
    em_BusinessVerificationStatus VARCHAR(1) DEFAULT 0, #0 is not verified, 1 is pending, 2 is verified

    FOREIGN KEY(em_id) REFERENCES users(ur_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE job_addresses(
    jbads_id VARCHAR(255) PRIMARY KEY,
    jbads_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    jbads_detail TEXT(20000) NOT NULL,
    jbads_em_id VARCHAR(255) NOT NULL,
    jbads_district VARCHAR(255) NOT NULL,
    jbads_isMajorAddress BOOLEAN NOT NULL,

    FOREIGN KEY (jbads_em_id) REFERENCES employers(em_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE job_types(
    jt_id VARCHAR(255) PRIMARY KEY,
    jt_name VARCHAR(36) NOT NULL,
    jt_description VARCHAR(20000) NOT NULL,
    jt_isApproved BOOLEAN NOT NULL,
    jt_submittedBy VARCHAR(255) NOT NULL,
    
    FOREIGN KEY (jt_submittedBy) REFERENCES employers(em_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE jobs(
    jb_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    jb_id VARCHAR(255) PRIMARY KEY,
    jb_title VARCHAR(255) NOT NULL,
    jb_description TEXT(20000) NOT NULL,
    jb_welfare TEXT(20000) NOT NULL,
    jb_jt_id VARCHAR(255) NOT NULL,
    jb_transportation TEXT(20000) NOT NULL,
    jb_requirement_language TEXT(50) NOT NULL,
    jb_requirement_dressing TEXT(200) NOT NULL,
    jb_requirement_other TEXT(200) NOT NULL,
    jb_isDeleted TINYINT(1) DEFAULT 0,
    jb_expected_payment_days INT(36) NOT NULL,
    jb_em_id VARCHAR(255) NOT NULL,
    jb_jbads_id VARCHAR(255) NOT NULL,

    FOREIGN KEY(jb_jt_id) REFERENCES job_types(jt_id),
    FOREIGN KEY (jb_em_id) REFERENCES employers(em_id),
    FOREIGN KEY (jb_jbads_id) REFERENCES job_addresses(jbads_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE job_qna(
	jbqna_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    jbqna_id VARCHAR(255) PRIMARY KEY,
    jbqna_jb_id VARCHAR(255) NOT NULL,
    jbqna_askedBy VARCHAR(255) NOT NULL, #freelancer
	jbqna_question TEXT(120) NOT NULL,
    jbqna_answer TEXT(120) NOT NULL,
    jbqna_isDeleted TINYINT(1) DEFAULT 0,
    
    FOREIGN KEY(jbqna_jb_id) REFERENCES jobs(jb_id),
    FOREIGN KEY(jbqna_askedBy) REFERENCES freelancers(fl_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE job_sessions(
    jbse_id VARCHAR(255) PRIMARY KEY,
    jbse_jb_id VARCHAR(255) NOT NULL,
    jbse_salary_amt INT(255) NOT NULL,
	jbse_salary_type TINYTEXT NOT NULL,
	jbse_endTime TIMESTAMP DEFAULT current_timestamp,
    jbse_startTime DATETIME DEFAULT current_timestamp,
    jbse_vacancy INT(36) NOT NULL,

    FOREIGN KEY(jbse_jb_id) REFERENCES jobs(jb_id),
    CONSTRAINT jbse_salary_type CHECK(
        jbse_salary_type IN ('hour rate','lump sum'))
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE job_applications(
    jbap_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    jbap_id VARCHAR(255) PRIMARY KEY,
    jbap_status TINYTEXT NOT NULL,
    jbap_isDeleted TINYINT(1) DEFAULT 0,
    jbap_jbse_id VARCHAR(255) NOT NULL,
    jbap_fl_id VARCHAR(255) NOT NULL,
    
    FOREIGN KEY(jbap_jbse_id) REFERENCES job_sessions(jbse_id),
    FOREIGN KEY(jbap_fl_id) REFERENCES freelancers(fl_id),

    CONSTRAINT jbap_status CHECK(
        jbap_status IN ('pending','rejected','accepted','withdrawed','completed','dispute','passed clearance','salary withdrawed')
        )
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE external_transactions(
	extr_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    extr_id VARCHAR(255) PRIMARY KEY,
    extr_paymentMethod TINYINT(1) NOT NULL,
    extr_paymentAmount float NOT NULL,
    extr_transactionType TINYINT(1) NOT NULL,
    extr_paymentInfo TEXT(200),
    extr_ur_id VARCHAR(255) NOT NULL,
    extr_status TINYTEXT NOT NULL,
    
    FOREIGN KEY(extr_ur_id) REFERENCES users(ur_id),
    CONSTRAINT extr_status CHECK(
        extr_status IN ('tbc1','tbc2','tbc3')
        )
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE chatrooms(
    chrm_id VARCHAR(255) PRIMARY KEY,
    chrm_jbse_id VARCHAR(255) NOT NULL,
    chrm_em_id VARCHAR(255) NOT NULL,
    chrm_status TINYTEXT NOT NULL,
    
    FOREIGN KEY(chrm_jbse_id) REFERENCES job_sessions(jbse_id),
    FOREIGN KEY(chrm_em_id) REFERENCES employers(em_id),
    
    CONSTRAINT chrm_status CHECK(
        chrm_status IN ('tbc1','tbc2','tbc3')
        )
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE chatroom_participants(
    parti_ur_id VARCHAR(255) NOT NULL,
    parti_chrm_id VARCHAR(255) NOT NULL,
    PRIMARY KEY(parti_ur_id, parti_chrm_id),
    parti_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY(parti_ur_id) REFERENCES users(ur_id),
    FOREIGN KEY(parti_chrm_id) REFERENCES chatrooms(chrm_id)
    
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE messages(
	msg_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    msg_id VARCHAR(255) PRIMARY KEY,
    msg_chrm_id VARCHAR(255) NOT NULL,
    msg_sentBy VARCHAR(255) NOT NULL,
    msg_content TEXT(180) NOT NULL,
    msg_status TINYTEXT NOT NULL,
    msg_type TINYINT(1) NOT NULL, #tbc
    
    FOREIGN KEY(msg_chrm_id) REFERENCES chatrooms(chrm_id),
    FOREIGN KEY(msg_sentBy) REFERENCES chatroom_participants(parti_ur_id),
    
    CONSTRAINT msg_status CHECK(
        msg_status IN ('tbc1','tbc2','tbc3')
        )
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE tags(
	tag_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    tag_id VARCHAR(255) PRIMARY KEY,
    tag_chrm_id VARCHAR(255),
    tag_sentBy VARCHAR(255) NOT NULL,
    tag_type TINYINT(1) NOT NULL, #tbc
    tag_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP, #state manually
    tag_status TINYTEXT NOT NULL,
    tag_isDeclined TINYINT(1) DEFAULT 0,
    tag_jbap_id VARCHAR(255) NOT NULL,
    
    FOREIGN KEY(tag_chrm_id) REFERENCES chatroom_participants(parti_chrm_id),
    FOREIGN KEY(tag_sentBy) REFERENCES chatroom_participants(parti_ur_id),
    FOREIGN KEY(tag_jbap_id) REFERENCES job_applications(jbap_id),
    
    CONSTRAINT tag_status CHECK(
        tag_status IN ('tbc1','tbc2','tbc3')
        )
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE clock_in_out(
	cinout_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    cinout_id VARCHAR(255) PRIMARY KEY,
    cinout_photo VARCHAR(2048),
    cinout_type TINYINT(1) NOT NULL, #tbc
    cinout_jbap_id VARCHAR(255) NOT NULL,
    
    FOREIGN KEY(cinout_jbap_id) REFERENCES job_applications(jbap_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE exit_surveys(
	exsv_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    exsv_id VARCHAR(255) PRIMARY KEY,
    exsv_jbse_id VARCHAR(255) NOT NULL,
    exsv_isEmployerFinished TINYINT(1) DEFAULT 0,
    exsv_isFreelancerFinished TINYINT(1) DEFAULT 0,
    
    FOREIGN KEY(exsv_jbse_id) REFERENCES job_sessions(jbse_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE rating_categories(
    ratecat_id VARCHAR(255) PRIMARY KEY,
    ratecat_name VARCHAR(36) NOT NULL,
    ratecat_description TEXT(300),
    ratecat_for TINYINT(1) NOT NULL #0 for freelancer, 1 for employer
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE ratings(
    rate_ratecat_id VARCHAR(255) NOT NULL,
    rate_exsv_id VARCHAR(255) NOT NULL,
    PRIMARY KEY(rate_ratecat_id, rate_exsv_id),
    rate_score INT(1) NOT NULL,

    FOREIGN KEY(rate_exsv_id) REFERENCES exit_surveys(exsv_id),
    FOREIGN KEY(rate_ratecat_id) REFERENCES rating_categories(ratecat_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE comment_categories(
    commcat_id VARCHAR(255) PRIMARY KEY,
    commcat_name VARCHAR(36) NOT NULL,
    commcat_description TEXT(300),
    commcat_for TINYINT(1) NOT NULL #0 for freelancer, 1 for employer
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE comments(
    comm_commcat_id VARCHAR(255) NOT NULL,
    comm_exsv_id VARCHAR(255) NOT NULL,
    PRIMARY KEY(comm_commcat_id, comm_exsv_id),
    comm_content TEXT(300) NOT NULL,

    FOREIGN KEY(comm_exsv_id) REFERENCES exit_surveys(exsv_id),
    FOREIGN KEY(comm_commcat_id) REFERENCES comment_categories(commcat_id)
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE internal_transactions(
	intr_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    intr_id VARCHAR(255) PRIMARY KEY,
    intr_from VARCHAR(255) NOT NULL,
    intr_to VARCHAR(255) NOT NULL,
    intr_paymentAmount FLOAT NOT NULL,
    intr_transactionType TINYINT(1) NOT NULL,
    intr_paymentInfo TEXT(200),
    intr_status TINYTEXT NOT NULL,
    
    FOREIGN KEY(intr_from) REFERENCES users(ur_id),
    FOREIGN KEY(intr_to) REFERENCES users(ur_id),
    
    CONSTRAINT intr_status CHECK(
        extr_status IN ('tbc1','tbc2','tbc3')
        )
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE reports(
	rep_creationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP on UPDATE CURRENT_TIMESTAMP,
    rep_id VARCHAR(255) PRIMARY KEY,
    rep_type TINYINT(1) NOT NULL,
    rep_from VARCHAR(255) NOT NULL,
    rep_targetUser VARCHAR(255),
    rep_targetJob VARCHAR(255),
    rep_description TEXT(200),
    rep_img VARCHAR(2048),
    rep_status TINYTEXT NOT NULL,
    
    FOREIGN KEY(rep_from) REFERENCES users(ur_id),
    FOREIGN KEY(rep_targetUser) REFERENCES users(ur_id),
    FOREIGN KEY(rep_targetJob) REFERENCES jobs(jb_id),
    
    CONSTRAINT rep_status CHECK(
        rep_status IN ('tbc1','tbc2','tbc3')
        )
)CHARACTER SET utf8 COLLATE utf8_unicode_ci;