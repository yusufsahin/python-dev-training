USE [StudentCourseCenterDb];
GO

SELECT * FROM dbo.Institutions;
SELECT * FROM dbo.AcademicTerms;
SELECT * FROM dbo.Students;
SELECT * FROM dbo.Teachers;
SELECT * FROM dbo.Courses;
SELECT * FROM dbo.ClassGroups;
SELECT * FROM dbo.StudentEnrollments;
SELECT * FROM dbo.LessonSchedules;
SELECT * FROM dbo.AttendanceRecords;
SELECT * FROM dbo.Exams;
SELECT * FROM dbo.ExamResults;
GO

SELECT * FROM dbo.vw_StudentEnrollmentDetails;
SELECT * FROM dbo.vw_TeacherSchedule;
SELECT * FROM dbo.vw_StudentExamResults;
GO

EXEC dbo.usp_RecordAttendance
    @ClassGroupId = 1,
    @StudentId = 1,
    @LessonDate = '2026-01-20',
    @AttendanceStatus = N'Present',
    @Note = N'On time';
GO

EXEC dbo.usp_SaveExamResult
    @ExamId = 1,
    @StudentId = 1,
    @Score = 90,
    @Note = N'Updated after review';
GO

SELECT * FROM dbo.AttendanceRecords;
SELECT * FROM dbo.ExamResults;
GO
