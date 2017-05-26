DROP TABLE IF EXISTS `registrations`;
DROP TABLE IF EXISTS `students`;
DROP TABLE IF EXISTS `sections`;
DROP TABLE IF EXISTS `courses`;
DROP TABLE IF EXISTS `faculty`;
DROP TABLE IF EXISTS `campuses`;
DROP TABLE IF EXISTS `terms`;

CREATE TABLE `terms` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `semester` VARCHAR(50) NOT NULL,
  `year` INT(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `campuses` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `location` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `faculty` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `is_adjunct` BOOL NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `courses` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `peoplesoft_course_id` VARCHAR(50) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `active` BOOL NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `sections` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `course_id` INT UNSIGNED NOT NULL,
  `term_id` INT UNSIGNED NOT NULL,
  `campus_id` INT UNSIGNED NOT NULL,
  `faculty_id` INT UNSIGNED NOT NULL,
  `section_number` INT(3) UNSIGNED ZEROFILL NOT NULL,
  `active` BOOL NOT NULL DEFAULT 1,
  `searchable` BOOL NOT NULL DEFAULT 1,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `credits` INT NOT NULL,
  `max_enrollment` INT NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (course_id) references courses(id) on DELETE CASCADE,
  FOREIGN KEY (term_id) references terms(id) on DELETE CASCADE,
  FOREIGN KEY (campus_id) references campuses(id) on DELETE CASCADE,
  FOREIGN KEY (faculty_id) references faculty(id) on DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `students` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `university_id` VARCHAR(50) NOT NULL,
  `net_id` VARCHAR(50) NOT NULL,
  `active` BOOL NOT NULL DEFAULT 1,
  `email` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `registrations` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `section_id` INT UNSIGNED NOT NULL,
  `student_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (section_id) references sections(id) on DELETE CASCADE,
  FOREIGN KEY (student_id) references students(id) on DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
