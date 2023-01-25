CREATE TABLE groups
(
    id VARCHAR(12) PRIMARY KEY,
    speciality_fk VARCHAR(8) NOT NULL
);

CREATE TABLE students
(
    id VARCHAR(8) PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    surname VARCHAR(20) NOT NULL,
    group_fk VARCHAR(12) NOT NULL,
    FOREIGN KEY (group_fk) REFERENCES groups (id)
);

CREATE TYPE lesson_type AS ENUM ('Практика', 'Лекция');
CREATE TABLE lessons
(
    id SERIAL PRIMARY KEY,
    type lesson_type NOT NULL,
    cource_fk INT NOT NULL,
    description_fk VARCHAR(50) NOT NULL
);

CREATE TABLE schedule(
    id SERIAL,
	groups_fk VARCHAR(12) REFERENCES groups (id) NOT NULL,
	lessons_fk INT REFERENCES lessons (id) NOT NULL,
	lesson_time TIMESTAMP NOT NULL
) PARTITION BY RANGE (lesson_time);

CREATE TABLE schedule_2019week1 PARTITION OF schedule
    FOR VALUES FROM ('2019-01-01') TO ('2019-01-06');

CREATE TABLE schedule_2019week2 PARTITION OF schedule
    FOR VALUES FROM ('2019-01-07') TO ('2019-01-13');

CREATE TABLE schedule_2019week3 PARTITION OF schedule
    FOR VALUES FROM ('2019-01-14') TO ('2019-01-20');

CREATE TABLE schedule_2019week4 PARTITION OF schedule
    FOR VALUES FROM ('2019-01-21') TO ('2019-01-27');

--CREATE TABLE schedule_2019week5 PARTITION OF schedule
--    FOR VALUES FROM ('2019-01-07') TO ('2019-01-13');

--CREATE TABLE schedule_2019week6 PARTITION OF schedule
--    FOR VALUES FROM ('2019-01-07') TO ('2019-01-13');

CREATE TABLE visits(
    id SERIAL PRIMARY KEY,
    visited boolean NOT NULL,
    student_fk VARCHAR(8) NOT NULL,
    schedule_fk INT NOT NULL,

    FOREIGN KEY (student_fk) REFERENCES students (id)
);