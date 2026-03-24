USE [StudentCourseCenterDb];
GO

/* =========================================================
   TABLES
   ========================================================= */

IF OBJECT_ID(N'dbo.Institutions', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Institutions
    (
        InstitutionId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        Name NVARCHAR(200) NOT NULL,
        Phone NVARCHAR(30) NULL,
        Email NVARCHAR(150) NULL,
        Address NVARCHAR(500) NULL,
        IsActive BIT NOT NULL CONSTRAINT DF_Institutions_IsActive DEFAULT (1),
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_Institutions_CreatedAt DEFAULT (SYSDATETIME())
    );
END
GO

IF OBJECT_ID(N'dbo.AcademicTerms', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.AcademicTerms
    (
        AcademicTermId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        InstitutionId INT NOT NULL,
        TermName NVARCHAR(100) NOT NULL,
        StartDate DATE NOT NULL,
        EndDate DATE NOT NULL,
        IsActive BIT NOT NULL CONSTRAINT DF_AcademicTerms_IsActive DEFAULT (1),
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_AcademicTerms_CreatedAt DEFAULT (SYSDATETIME()),

        CONSTRAINT FK_AcademicTerms_Institutions
            FOREIGN KEY (InstitutionId) REFERENCES dbo.Institutions(InstitutionId),

        CONSTRAINT CHK_AcademicTerms_DateRange
            CHECK (StartDate <= EndDate)
    );
END
GO

IF OBJECT_ID(N'dbo.Students', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Students
    (
        StudentId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        InstitutionId INT NOT NULL,
        StudentNo NVARCHAR(30) NOT NULL,
        FirstName NVARCHAR(100) NOT NULL,
        LastName NVARCHAR(100) NOT NULL,
        BirthDate DATE NULL,
        Gender NVARCHAR(20) NULL,
        Phone NVARCHAR(30) NULL,
        Email NVARCHAR(150) NULL,
        SchoolName NVARCHAR(200) NULL,
        GradeLevel INT NULL,
        IsActive BIT NOT NULL CONSTRAINT DF_Students_IsActive DEFAULT (1),
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_Students_CreatedAt DEFAULT (SYSDATETIME()),

        CONSTRAINT FK_Students_Institutions
            FOREIGN KEY (InstitutionId) REFERENCES dbo.Institutions(InstitutionId),

        CONSTRAINT UQ_Students_Institution_StudentNo
            UNIQUE (InstitutionId, StudentNo)
    );
END
GO

IF OBJECT_ID(N'dbo.Teachers', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Teachers
    (
        TeacherId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        InstitutionId INT NOT NULL,
        TeacherNo NVARCHAR(30) NOT NULL,
        FirstName NVARCHAR(100) NOT NULL,
        LastName NVARCHAR(100) NOT NULL,
        Phone NVARCHAR(30) NULL,
        Email NVARCHAR(150) NULL,
        HireDate DATE NULL,
        IsActive BIT NOT NULL CONSTRAINT DF_Teachers_IsActive DEFAULT (1),
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_Teachers_CreatedAt DEFAULT (SYSDATETIME()),

        CONSTRAINT FK_Teachers_Institutions
            FOREIGN KEY (InstitutionId) REFERENCES dbo.Institutions(InstitutionId),

        CONSTRAINT UQ_Teachers_Institution_TeacherNo
            UNIQUE (InstitutionId, TeacherNo)
    );
END
GO

IF OBJECT_ID(N'dbo.Courses', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Courses
    (
        CourseId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        InstitutionId INT NOT NULL,
        CourseCode NVARCHAR(30) NOT NULL,
        CourseName NVARCHAR(150) NOT NULL,
        Description NVARCHAR(500) NULL,
        IsActive BIT NOT NULL CONSTRAINT DF_Courses_IsActive DEFAULT (1),
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_Courses_CreatedAt DEFAULT (SYSDATETIME()),

        CONSTRAINT FK_Courses_Institutions
            FOREIGN KEY (InstitutionId) REFERENCES dbo.Institutions(InstitutionId),

        CONSTRAINT UQ_Courses_Institution_CourseCode
            UNIQUE (InstitutionId, CourseCode)
    );
END
GO

IF OBJECT_ID(N'dbo.TeacherCourses', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.TeacherCourses
    (
        TeacherCourseId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        TeacherId INT NOT NULL,
        CourseId INT NOT NULL,
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_TeacherCourses_CreatedAt DEFAULT (SYSDATETIME()),

        CONSTRAINT FK_TeacherCourses_Teachers
            FOREIGN KEY (TeacherId) REFERENCES dbo.Teachers(TeacherId),

        CONSTRAINT FK_TeacherCourses_Courses
            FOREIGN KEY (CourseId) REFERENCES dbo.Courses(CourseId),

        CONSTRAINT UQ_TeacherCourses_Teacher_Course
            UNIQUE (TeacherId, CourseId)
    );
END
GO

IF OBJECT_ID(N'dbo.ClassGroups', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.ClassGroups
    (
        ClassGroupId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        InstitutionId INT NOT NULL,
        AcademicTermId INT NOT NULL,
        CourseId INT NOT NULL,
        TeacherId INT NOT NULL,
        GroupCode NVARCHAR(30) NOT NULL,
        GroupName NVARCHAR(150) NOT NULL,
        Capacity INT NOT NULL CONSTRAINT DF_ClassGroups_Capacity DEFAULT (20),
        Classroom NVARCHAR(50) NULL,
        IsActive BIT NOT NULL CONSTRAINT DF_ClassGroups_IsActive DEFAULT (1),
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_ClassGroups_CreatedAt DEFAULT (SYSDATETIME()),

        CONSTRAINT FK_ClassGroups_Institutions
            FOREIGN KEY (InstitutionId) REFERENCES dbo.Institutions(InstitutionId),

        CONSTRAINT FK_ClassGroups_AcademicTerms
            FOREIGN KEY (AcademicTermId) REFERENCES dbo.AcademicTerms(AcademicTermId),

        CONSTRAINT FK_ClassGroups_Courses
            FOREIGN KEY (CourseId) REFERENCES dbo.Courses(CourseId),

        CONSTRAINT FK_ClassGroups_Teachers
            FOREIGN KEY (TeacherId) REFERENCES dbo.Teachers(TeacherId),

        CONSTRAINT UQ_ClassGroups_Institution_GroupCode
            UNIQUE (InstitutionId, GroupCode),

        CONSTRAINT CHK_ClassGroups_Capacity
            CHECK (Capacity > 0)
    );
END
GO

IF OBJECT_ID(N'dbo.StudentEnrollments', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.StudentEnrollments
    (
        StudentEnrollmentId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        StudentId INT NOT NULL,
        ClassGroupId INT NOT NULL,
        EnrollDate DATE NOT NULL CONSTRAINT DF_StudentEnrollments_EnrollDate DEFAULT (CAST(GETDATE() AS DATE)),
        EnrollmentStatus NVARCHAR(20) NOT NULL CONSTRAINT DF_StudentEnrollments_Status DEFAULT (N'Active'),
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_StudentEnrollments_CreatedAt DEFAULT (SYSDATETIME()),

        CONSTRAINT FK_StudentEnrollments_Students
            FOREIGN KEY (StudentId) REFERENCES dbo.Students(StudentId),

        CONSTRAINT FK_StudentEnrollments_ClassGroups
            FOREIGN KEY (ClassGroupId) REFERENCES dbo.ClassGroups(ClassGroupId),

        CONSTRAINT UQ_StudentEnrollments_Student_ClassGroup
            UNIQUE (StudentId, ClassGroupId),

        CONSTRAINT CHK_StudentEnrollments_Status
            CHECK (EnrollmentStatus IN (N'Active', N'Left', N'Completed'))
    );
END
GO

IF OBJECT_ID(N'dbo.LessonSchedules', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.LessonSchedules
    (
        LessonScheduleId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        ClassGroupId INT NOT NULL,
        DayOfWeek TINYINT NOT NULL,
        StartTime TIME(0) NOT NULL,
        EndTime TIME(0) NOT NULL,
        Room NVARCHAR(50) NULL,
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_LessonSchedules_CreatedAt DEFAULT (SYSDATETIME()),

        CONSTRAINT FK_LessonSchedules_ClassGroups
            FOREIGN KEY (ClassGroupId) REFERENCES dbo.ClassGroups(ClassGroupId),

        CONSTRAINT CHK_LessonSchedules_DayOfWeek
            CHECK (DayOfWeek BETWEEN 1 AND 7),

        CONSTRAINT CHK_LessonSchedules_Time
            CHECK (StartTime < EndTime)
    );
END
GO

IF OBJECT_ID(N'dbo.AttendanceRecords', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.AttendanceRecords
    (
        AttendanceRecordId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        ClassGroupId INT NOT NULL,
        StudentId INT NOT NULL,
        LessonDate DATE NOT NULL,
        AttendanceStatus NVARCHAR(20) NOT NULL,
        Note NVARCHAR(300) NULL,
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_AttendanceRecords_CreatedAt DEFAULT (SYSDATETIME()),

        CONSTRAINT FK_AttendanceRecords_ClassGroups
            FOREIGN KEY (ClassGroupId) REFERENCES dbo.ClassGroups(ClassGroupId),

        CONSTRAINT FK_AttendanceRecords_Students
            FOREIGN KEY (StudentId) REFERENCES dbo.Students(StudentId),

        CONSTRAINT UQ_AttendanceRecords_Group_Student_Date
            UNIQUE (ClassGroupId, StudentId, LessonDate),

        CONSTRAINT CHK_AttendanceRecords_Status
            CHECK (AttendanceStatus IN (N'Present', N'Absent', N'Late', N'Excused'))
    );
END
GO

IF OBJECT_ID(N'dbo.Exams', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Exams
    (
        ExamId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        ClassGroupId INT NOT NULL,
        ExamName NVARCHAR(150) NOT NULL,
        ExamDate DATE NOT NULL,
        TotalScore DECIMAL(5,2) NOT NULL CONSTRAINT DF_Exams_TotalScore DEFAULT (100),
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_Exams_CreatedAt DEFAULT (SYSDATETIME()),

        CONSTRAINT FK_Exams_ClassGroups
            FOREIGN KEY (ClassGroupId) REFERENCES dbo.ClassGroups(ClassGroupId),

        CONSTRAINT CHK_Exams_TotalScore
            CHECK (TotalScore > 0)
    );
END
GO

IF OBJECT_ID(N'dbo.ExamResults', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.ExamResults
    (
        ExamResultId INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        ExamId INT NOT NULL,
        StudentId INT NOT NULL,
        Score DECIMAL(5,2) NOT NULL,
        Note NVARCHAR(300) NULL,
        CreatedAt DATETIME2(0) NOT NULL CONSTRAINT DF_ExamResults_CreatedAt DEFAULT (SYSDATETIME()),

        CONSTRAINT FK_ExamResults_Exams
            FOREIGN KEY (ExamId) REFERENCES dbo.Exams(ExamId),

        CONSTRAINT FK_ExamResults_Students
            FOREIGN KEY (StudentId) REFERENCES dbo.Students(StudentId),

        CONSTRAINT UQ_ExamResults_Exam_Student
            UNIQUE (ExamId, StudentId)
    );
END
GO

/* =========================================================
   INDEXES
   ========================================================= */

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_Students_InstitutionId' AND object_id = OBJECT_ID(N'dbo.Students'))
    CREATE INDEX IX_Students_InstitutionId ON dbo.Students(InstitutionId);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_Teachers_InstitutionId' AND object_id = OBJECT_ID(N'dbo.Teachers'))
    CREATE INDEX IX_Teachers_InstitutionId ON dbo.Teachers(InstitutionId);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_Courses_InstitutionId' AND object_id = OBJECT_ID(N'dbo.Courses'))
    CREATE INDEX IX_Courses_InstitutionId ON dbo.Courses(InstitutionId);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_ClassGroups_AcademicTermId' AND object_id = OBJECT_ID(N'dbo.ClassGroups'))
    CREATE INDEX IX_ClassGroups_AcademicTermId ON dbo.ClassGroups(AcademicTermId);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_ClassGroups_CourseId' AND object_id = OBJECT_ID(N'dbo.ClassGroups'))
    CREATE INDEX IX_ClassGroups_CourseId ON dbo.ClassGroups(CourseId);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_ClassGroups_TeacherId' AND object_id = OBJECT_ID(N'dbo.ClassGroups'))
    CREATE INDEX IX_ClassGroups_TeacherId ON dbo.ClassGroups(TeacherId);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_StudentEnrollments_StudentId' AND object_id = OBJECT_ID(N'dbo.StudentEnrollments'))
    CREATE INDEX IX_StudentEnrollments_StudentId ON dbo.StudentEnrollments(StudentId);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_StudentEnrollments_ClassGroupId' AND object_id = OBJECT_ID(N'dbo.StudentEnrollments'))
    CREATE INDEX IX_StudentEnrollments_ClassGroupId ON dbo.StudentEnrollments(ClassGroupId);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_AttendanceRecords_StudentId' AND object_id = OBJECT_ID(N'dbo.AttendanceRecords'))
    CREATE INDEX IX_AttendanceRecords_StudentId ON dbo.AttendanceRecords(StudentId);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_AttendanceRecords_ClassGroup_LessonDate' AND object_id = OBJECT_ID(N'dbo.AttendanceRecords'))
    CREATE INDEX IX_AttendanceRecords_ClassGroup_LessonDate ON dbo.AttendanceRecords(ClassGroupId, LessonDate);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_ExamResults_StudentId' AND object_id = OBJECT_ID(N'dbo.ExamResults'))
    CREATE INDEX IX_ExamResults_StudentId ON dbo.ExamResults(StudentId);
GO
