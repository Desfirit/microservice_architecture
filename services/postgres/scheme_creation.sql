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
    course_fk VARCHAR(100) NOT NULL,
    description_fk VARCHAR(50) NOT NULL
);

CREATE TABLE schedule(
    id SERIAL,
	group_fk VARCHAR(12) REFERENCES groups (id) NOT NULL,
	lesson_fk INT REFERENCES lessons (id) NOT NULL,
	time TIMESTAMP NOT NULL
) PARTITION BY RANGE (time);

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

--Посчитать посещение и прогулы студентов
SELECT student_fk, visited, COUNT(visited) FROM visits GROUP BY student_fk, visited ORDER BY student_fk;

--Посчитать частоту прогулов и вывести в порядке худших
SELECT student_fk, CAST(COUNT(CASE visited WHEN true THEN 1 ELSE NULL END) AS FLOAT) / COUNT(*) AS visit_percent FROM visits GROUP BY student_fk ORDER BY visit_percent;

--Посчитать частоту прогулов и вывести в порядке худших по определенным лекциям
SELECT student_fk, CAST(COUNT(CASE visited WHEN true THEN 1 ELSE NULL END) AS FLOAT) / COUNT(*) AS visit_percent 
FROM visits JOIN schedule ON visits.schedule_fk = schedule.id 
WHERE schedule.lesson_fk IN (1,3)
GROUP BY student_fk 
ORDER BY visit_percent;

--Посчитать частоту прогулов и вывести в порядке худших по определенным лекциям и в промежутке
SELECT student_fk, CAST(COUNT(CASE visited WHEN true THEN 1 ELSE NULL END) AS FLOAT) / COUNT(*) AS visit_percent 
FROM visits JOIN schedule ON visits.schedule_fk = schedule.id 
WHERE schedule.lesson_fk IN (1,3) AND schedule.time BETWEEN '2019-02-04 09:00:00' AND '2019-09-10 16:20:00'
GROUP BY student_fk 
ORDER BY visit_percent;

--Посчитать топ 10 частоту прогулов и вывести в порядке худших по определенным лекциям и в промежутке
SELECT student_fk AS id, CAST(COUNT(CASE visited WHEN true THEN 1 ELSE NULL END) AS FLOAT) / COUNT(*) AS visit_percent 
FROM visits JOIN schedule ON visits.schedule_fk = schedule.id 
WHERE schedule.lesson_fk IN (1,3) AND schedule.time BETWEEN '2019-02-04 09:00:00' AND '2019-09-10 16:20:00'
GROUP BY student_fk 
ORDER BY visit_percent
LIMIT 10;