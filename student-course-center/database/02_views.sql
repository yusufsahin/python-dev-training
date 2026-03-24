USE [StudentCourseCenterDb];
GO

CREATE OR ALTER VIEW dbo.vw_StudentEnrollmentDetails
AS
SELECT
    se.StudentEnrollmentId,
    s.StudentId,
    s.StudentNo,
    s.FirstName,
    s.LastName,
    cg.ClassGroupId,
    cg.GroupCode,
    cg.GroupName,
    c.CourseName,
    t.FirstName + N' ' + t.LastName AS TeacherName,
    at.TermName,
    se.EnrollDate,
    se.EnrollmentStatus
FROM dbo.StudentEnrollments se
INNER JOIN dbo.Students s ON s.StudentId = se.StudentId
INNER JOIN dbo.ClassGroups cg ON cg.ClassGroupId = se.ClassGroupId
INNER JOIN dbo.Courses c ON c.CourseId = cg.CourseId
INNER JOIN dbo.Teachers t ON t.TeacherId = cg.TeacherId
INNER JOIN dbo.AcademicTerms at ON at.AcademicTermId = cg.AcademicTermId;
GO

CREATE OR ALTER VIEW dbo.vw_TeacherSchedule
AS
SELECT
    t.TeacherId,
    t.TeacherNo,
    t.FirstName,
    t.LastName,
    cg.ClassGroupId,
    cg.GroupCode,
    cg.GroupName,
    c.CourseName,
    ls.DayOfWeek,
    ls.StartTime,
    ls.EndTime,
    ls.Room
FROM dbo.ClassGroups cg
INNER JOIN dbo.Teachers t ON t.TeacherId = cg.TeacherId
INNER JOIN dbo.Courses c ON c.CourseId = cg.CourseId
LEFT JOIN dbo.LessonSchedules ls ON ls.ClassGroupId = cg.ClassGroupId;
GO

CREATE OR ALTER VIEW dbo.vw_StudentExamResults
AS
SELECT
    s.StudentId,
    s.StudentNo,
    s.FirstName,
    s.LastName,
    e.ExamId,
    e.ExamName,
    e.ExamDate,
    e.TotalScore,
    er.Score,
    CAST((er.Score * 100.0) / NULLIF(e.TotalScore, 0) AS DECIMAL(5,2)) AS Percentage,
    cg.GroupName,
    c.CourseName
FROM dbo.ExamResults er
INNER JOIN dbo.Exams e ON e.ExamId = er.ExamId
INNER JOIN dbo.Students s ON s.StudentId = er.StudentId
INNER JOIN dbo.ClassGroups cg ON cg.ClassGroupId = e.ClassGroupId
INNER JOIN dbo.Courses c ON c.CourseId = cg.CourseId;
GO
