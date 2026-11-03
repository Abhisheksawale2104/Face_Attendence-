CREATE TABLE IF NOT EXISTS people (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    full_name VARCHAR(120) NOT NULL,
    image_path VARCHAR(500) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS attendance_records (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    person_id INT UNSIGNED NOT NULL,
    attended_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    recognition_confidence DECIMAL(5, 4) NULL,
    PRIMARY KEY (id),
    INDEX idx_attendance_person_time (person_id, attended_at),
    CONSTRAINT fk_attendance_person
        FOREIGN KEY (person_id) REFERENCES people (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
