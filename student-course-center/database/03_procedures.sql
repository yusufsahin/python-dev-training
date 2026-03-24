USE [StudentCourseCenterDb];
GO

CREATE OR ALTER PROCEDURE dbo.usp_EnrollStudentToClassGroup
    @StudentId INT,
    @ClassGroupId INT
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM dbo.Students WHERE StudentId = @StudentId AND IsActive = 1)
    BEGIN
        THROW 50001, N'Student not found or inactive.', 1;
    END

    IF NOT EXISTS (SELECT 1 FROM dbo.ClassGroups WHERE ClassGroupId = @ClassGroupId AND IsActive = 1)
    BEGIN
        THROW 50002, N'Class group not found or inactive.', 1;
    END

    IF EXISTS
    (
        SELECT 1
        FROM dbo.StudentEnrollments
        WHERE StudentId = @StudentId
          AND ClassGroupId = @ClassGroupId
    )
    BEGIN
        THROW 50003, N'Student is already enrolled in this class group.', 1;
    END

    DECLARE @Capacity INT;
    DECLARE @CurrentActiveCount INT;

    SELECT @Capacity = Capacity
    FROM dbo.ClassGroups
    WHERE ClassGroupId = @ClassGroupId;

    SELECT @CurrentActiveCount = COUNT(*)
    FROM dbo.StudentEnrollments
    WHERE ClassGroupId = @ClassGroupId
      AND EnrollmentStatus = N'Active';

    IF @CurrentActiveCount >= @Capacity
    BEGIN
        THROW 50004, N'Class group capacity exceeded.', 1;
    END

    INSERT INTO dbo.StudentEnrollments
    (
        StudentId,
        ClassGroupId,
        EnrollmentStatus
    )
    VALUES
    (
        @StudentId,
        @ClassGroupId,
        N'Active'
    );
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_RecordAttendance
    @ClassGroupId INT,
    @StudentId INT,
    @LessonDate DATE,
    @AttendanceStatus NVARCHAR(20),
    @Note NVARCHAR(300) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    IF @AttendanceStatus NOT IN (N'Present', N'Absent', N'Late', N'Excused')
    BEGIN
        THROW 50005, N'Invalid attendance status.', 1;
    END

    IF NOT EXISTS
    (
        SELECT 1
        FROM dbo.StudentEnrollments
        WHERE StudentId = @StudentId
          AND ClassGroupId = @ClassGroupId
          AND EnrollmentStatus = N'Active'
    )
    BEGIN
        THROW 50006, N'Student is not actively enrolled in this class group.', 1;
    END

    IF EXISTS
    (
        SELECT 1
        FROM dbo.AttendanceRecords
        WHERE ClassGroupId = @ClassGroupId
          AND StudentId = @StudentId
          AND LessonDate = @LessonDate
    )
    BEGIN
        UPDATE dbo.AttendanceRecords
        SET AttendanceStatus = @AttendanceStatus,
            Note = @Note
        WHERE ClassGroupId = @ClassGroupId
          AND StudentId = @StudentId
          AND LessonDate = @LessonDate;
    END
    ELSE
    BEGIN
        INSERT INTO dbo.AttendanceRecords
        (
            ClassGroupId,
            StudentId,
            LessonDate,
            AttendanceStatus,
            Note
        )
        VALUES
        (
            @ClassGroupId,
            @StudentId,
            @LessonDate,
            @AttendanceStatus,
            @Note
        );
    END
END
GO

CREATE OR ALTER PROCEDURE dbo.usp_SaveExamResult
    @ExamId INT,
    @StudentId INT,
    @Score DECIMAL(5,2),
    @Note NVARCHAR(300) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @TotalScore DECIMAL(5,2);

    SELECT @TotalScore = TotalScore
    FROM dbo.Exams
    WHERE ExamId = @ExamId;

    IF @TotalScore IS NULL
    BEGIN
        THROW 50007, N'Exam not found.', 1;
    END

    IF @Score < 0 OR @Score > @TotalScore
    BEGIN
        THROW 50008, N'Score cannot be less than 0 or greater than total score.', 1;
    END

    IF EXISTS
    (
        SELECT 1
        FROM dbo.ExamResults
        WHERE ExamId = @ExamId
          AND StudentId = @StudentId
    )
    BEGIN
        UPDATE dbo.ExamResults
        SET Score = @Score,
            Note = @Note
        WHERE ExamId = @ExamId
          AND StudentId = @StudentId;
    END
    ELSE
    BEGIN
        INSERT INTO dbo.ExamResults
        (
            ExamId,
            StudentId,
            Score,
            Note
        )
        VALUES
        (
            @ExamId,
            @StudentId,
            @Score,
            @Note
        );
    END
END
GO
