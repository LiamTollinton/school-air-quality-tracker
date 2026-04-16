# Case Specification: Air Quality Concern Report

This document defines the required and optional fields for cases raised by schools or parents regarding air quality concerns.

## Case Submission Fields

### Submitter Information
- **Submitter Name** (Required)
  - Type: String
  - Description: Full name of the person reporting the case
  
- **Submitter Role** (Required)
  - Type: Enum: [Parent, Student, Teacher, Staff, School Administrator, Other]
  - Description: Role or position of the submitter within or related to the school

- **Contact Email** (Required)
  - Type: Email
  - Description: Valid email address for follow-up communication

- **Contact Phone** (Optional)
  - Type: String (formatted)
  - Description: Phone number for urgent communication

### Case Details

- **School/Building Name** (Required)
  - Type: String
  - Description: Name of the affected school or educational facility

- **Building Location/Room** (Required)
  - Type: String
  - Description: Specific location within the school (e.g., "Room 301", "Main Gymnasium", "Building A - 2nd Floor")

- **Date/Time of Incident** (Required)
  - Type: DateTime
  - Description: When the air quality concern was first noticed

- **Issue Category** (Required)
  - Type: Enum: [Odor, Dust/Particles, Mold/Moisture, Chemical Smell, Poor Ventilation, Temperature Issues, Other]
  - Description: General category of the air quality issue

- **Detailed Description** (Required)
  - Type: Long Text
  - Min Length: 50 characters
  - Description: Detailed account of the air quality issue and circumstances

### Health & Environmental Impact

- **Health Symptoms Observed** (Optional)
  - Type: Multi-select: [Headaches, Respiratory Issues, Eye Irritation, Dizziness, Nausea, Allergic Reactions, Fatigue, Other]
  - Description: Any health impacts associated with the air quality issue

- **Number of People Affected** (Optional)
  - Type: Integer
  - Description: Approximate count of individuals impacted by the condition

- **Duration of Issue** (Optional)
  - Type: String
  - Examples: "30 minutes", "Several hours", "Multiple days", "Ongoing"
  - Description: How long the problem has been occurring

- **Environmental Observations** (Optional)
  - Type: Multi-select: [Visible Dust, Visible Mold, Condensation, Discoloration, Debris, Other]
  - Description: Observable environmental conditions contributing to the concern

### Severity & Priority

- **Severity Level** (Required)
  - Type: Enum: [Low, Medium, High, Critical]
  - Guidance:
    - Low: Occasional odor, minimal impact
    - Medium: Persistent issue affecting classroom activities
    - High: Multiple people affected, noticeable health symptoms
    - Critical: Serious health symptoms, widespread impact, immediate action needed

- **Urgency** (Required)
  - Type: Boolean (Is this urgent?)
  - Description: Requires immediate attention

### Evidence & Documentation

- **Photo/Video Attachments** (Optional)
  - Type: File Upload (supports: jpg, png, gif, mp4, mov)
  - Max File Size: 25MB per file, up to 5 files
  - Description: Visual evidence of the air quality issue

- **Supporting Documents** (Optional)
  - Type: File Upload (supports: pdf, doc, docx)
  - Max File Size: 10MB per file, up to 3 files
  - Description: Medical reports, maintenance records, test results, etc.

### Administrative Reference

- **Related Incidents** (Optional)
  - Type: String (comma-separated case IDs)
  - Description: IDs of any related or previous cases about the same location

- **Previous Reports About This Location** (Auto-populated)
  - Type: Boolean
  - Description: Whether this location has had prior air quality reports

## Case Status & Workflow Fields

### Internal Use (Populated by School/Admin)

- **Case ID** (Auto-generated)
  - Type: String
  - Format: AQT-YYYY-MM-XXXXX
  - Description: Unique identifier for tracking

- **Assigned To** (Optional)
  - Type: User/Staff Reference
  - Description: School administrator responsible for the case

- **Status** (Required, Default: Open)
  - Type: Enum: [Open, Investigating, In Progress, Resolved, Closed, On Hold]
  - Description: Current status of the case

- **Resolution Date** (Conditional, required if Status = Resolved/Closed)
  - Type: Date
  - Description: When the issue was resolved

- **Internal Notes** (Optional)
  - Type: Long Text
  - Description: Administrative comments not visible to submitter

- **Actions Taken** (Optional)
  - Type: Long Text
  - Description: Detailed record of investigation and remediation steps

- **Follow-up Date** (Optional)
  - Type: Date
  - Description: When to follow up with the submitter

## Data Validation Rules

- Email must be valid and unique per submission
- Submitter name must be at least 2 characters
- Detailed description must be substantive (50+ characters)
- Building location cannot be empty
- Severity level and urgency must be set before case closure

## Submission Workflow

1. User fills out all required fields
2. System validates input and checks for duplicate/related cases
3. Case is submitted with auto-generated Case ID
4. Confirmation email sent to submitter
5. Case added to school administrator queue for review
6. Administrator can reach out with follow-up questions if needed
