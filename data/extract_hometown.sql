ATTACH DATABASE "database.db" AS full;
CREATE TABLE main.hometown
AS SELECT category, img, name, hometown, college, medicalschool, careerplans, bio, popup, hometownlatitude AS "latitude", hometownlongitude AS "longitude"
FROM full.resident
where hometownlatitude NOTNULL;
