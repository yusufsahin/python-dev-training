USE [StudentCourseCenterDb];
GO

/* Institution */
IF NOT EXISTS (SELECT 1 FROM dbo.Institutions WHERE Name = N'Basari Dershanesi')
BEGIN
    INSERT INTO dbo.Institutions (Name, Phone, Email, Address)
    VALUES (N'Basari Dershanesi', N'0212 000 00 00', N'info@basari.com', N'Istanbul');
END
GO

/* Academic Term */
IF NOT EXISTS (SELECT 1 FROM dbo.AcademicTerms WHERE TermName = N'2025-2026')
BEGIN
    INSERT INTO dbo.AcademicTerms (InstitutionId, TermName, StartDate, EndDate)
    VALUES (1, N'2025-2026', '2025-09-01', '2026-06-30');
END
GO

/* Students */
IF NOT EXISTS (SELECT 1 FROM dbo.Students WHERE StudentNo = N'STU001')
BEGIN
    INSERT INTO dbo.Students (InstitutionId, StudentNo, FirstName, LastName, GradeLevel, SchoolName, Phone)
    VALUES 
    (1, N'STU001', N'Ahmet', N'Yilmaz', 11, N'Ataturk Lisesi', N'05000000001'),
    (1, N'STU002', N'Ayse', N'Kaya', 12, N'Cumhuriyet Lisesi', N'05000000002'),
    (1, N'STU003', N'Mehmet', N'Can', 10, N'Anadolu Lisesi', N'05000000003');
END
GO

/* Teachers */
IF NOT EXISTS (SELECT 1 FROM dbo.Teachers WHERE TeacherNo = N'TCH001')
BEGIN
    INSERT INTO dbo.Teachers (InstitutionId, TeacherNo, FirstName, LastName, Phone)
    VALUES
    (1, N'TCH001', N'Elif', N'Demir', N'05000000101'),
    (1, N'TCH002', N'Can', N'Arslan', N'05000000102');
END
GO

/* Courses */
IF NOT EXISTS (SELECT 1 FROM dbo.Courses WHERE CourseCode = N'MAT')
BEGIN
    INSERT INTO dbo.Courses (InstitutionId, CourseCode, CourseName)
    VALUES
    (1, N'MAT', N'Matematik'),
    (1, N'FIZ', N'Fizik'),
    (1, N'KIM', N'Kimya');
END
GO

/* TeacherCourses */
IF NOT EXISTS (SELECT 1 FROM dbo.TeacherCourses WHERE TeacherId = 1 AND CourseId = 1)
BEGIN
    INSERT INTO dbo.TeacherCourses (TeacherId, CourseId)
    VALUES
    (1, 1),
    (2, 2),
    (2, 3);
END
GO

/* ClassGroups */
IF NOT EXISTS (SELECT 1 FROM dbo.ClassGroups WHERE GroupCode = N'MAT-11-A')
BEGIN
    INSERT INTO dbo.ClassGroups
    (
        InstitutionId,
        AcademicTermId,
        CourseId,
        TeacherId,
        GroupCode,
        GroupName,
        Capacity,
        Classroom
    )
    VALUES
    (1, 1, 1, 1, N'MAT-11-A', N'11 Sinif Matematik A', 25, N'A1'),
    (1, 1, 2, 2, N'FIZ-12-A', N'12 Sinif Fizik A', 20, N'B2');
END
GO

/* Student Enrollments */
IF NOT EXISTS (SELECT 1 FROM dbo.StudentEnrollments WHERE StudentId = 1 AND ClassGroupId = 1)
BEGIN
    INSERT INTO dbo.StudentEnrollments (StudentId, ClassGroupId, EnrollmentStatus)
    VALUES
    (1, 1, N'Active'),
    (2, 1, N'Active'),
    (2, 2, N'Active'),
    (3, 1, N'Active');
END
GO

/* Lesson Schedules */
IF NOT EXISTS (SELECT 1 FROM dbo.LessonSchedules WHERE ClassGroupId = 1 AND DayOfWeek = 1)
BEGIN
    INSERT INTO dbo.LessonSchedules (ClassGroupId, DayOfWeek, StartTime, EndTime, Room)
    VALUES
    (1, 1, '09:00', '10:30', N'A1'),
    (1, 3, '09:00', '10:30', N'A1'),
    (2, 2, '11:00', '12:30', N'B2');
END
GO

/* Exams */
IF NOT EXISTS (SELECT 1 FROM dbo.Exams WHERE ExamName = N'Matematik Quiz 1')
BEGIN
    INSERT INTO dbo.Exams (ClassGroupId, ExamName, ExamDate, TotalScore)
    VALUES
    (1, N'Matematik Quiz 1', '2026-01-10', 100),
    (2, N'Fizik Quiz 1', '2026-01-15', 100);
END
GO

/* Exam Results */
IF NOT EXISTS (SELECT 1 FROM dbo.ExamResults WHERE ExamId = 1 AND StudentId = 1)
BEGIN
    INSERT INTO dbo.ExamResults (ExamId, StudentId, Score, Note)
    VALUES
    (1, 1, 85, N'Good'),
    (1, 2, 92, N'Very Good'),
    (1, 3, 74, N'Needs improvement'),
    (2, 2, 88, N'Stable');
END
GO
