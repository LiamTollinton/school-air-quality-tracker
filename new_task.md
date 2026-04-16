Integrate Air Quality Concern Report into Existing Caseworker UI
Objective

Extend the existing Caseworker UI and backend so it supports a new case type: air_quality_concern, while preserving the current generic case management experience.

Context

We already have an existing caseworker application with:

Dashboard
Case list
Case detail page
Timeline / notes
Policy guidance panel
Workflow status tracking
Team leader dashboard

Add a specialist workflow for school air quality complaints raised by parents, staff, or schools.

Functional Requirements
1. New Case Type

Add support for:

air_quality_concern

This case type should appear alongside existing case types.

2. Create Case Form

Build a submission form with these sections:

Submitter Information
submitter_name (required)
submitter_role (Parent, Student, Teaching Staff, Facilities Staff, Admin Staff, Other)
contact_email (required)
contact_phone (optional)
Location
school_name (required)
building_location_room (required)
Incident Details
incident_datetime (required)
issue_category (Odor, Dust/Particles, Mold/Moisture, Chemical Smell, Poor Ventilation, Temperature Issues, Other)
detailed_description (required, min 50 chars)
Health Impact
symptoms (multi-select)
affected_count
duration
Environmental Observations
observations (multi-select)
Severity
severity_level (Low, Medium, High, Critical)
urgency (boolean)
Evidence Uploads
photos/videos
supporting_documents
Related Cases
related_incidents

On submit:

validate required fields
generate case_id format: AQT-YYYY-MM-XXXXX
set status = Open
add to admin queue
show confirmation message
3. Case Detail Page Enhancements

When case_type = air_quality_concern, render these panels:

Summary Card

Show:

school n- room/location
issue type
severity
urgent yes/no
current status
Incident Description

Full user description.

Symptoms & Impact

Badges/list of symptoms and affected people.

Evidence Panel

Preview attachments.

Timeline

Reuse existing timeline component.

Internal Actions
notes
actions_taken
assigned_to
follow_up_date
Policy Guidance Panel

Show matched guidance based on issue_category and severity. Examples:

Mold -> inspection within SLA n- Poor Ventilation -> CO2 assessment
Critical -> same-day escalation
Recommended Next Actions (mock AI or rules)

Examples:

Request facilities inspection
Contact submitter
Arrange classroom air test
Escalate to team leader
4. Dashboard Updates

Add widgets:

Open air quality cases
Critical cases
Cases by school
SLA breaches
Cases by severity
5. Team Leader View

Add:

workload by officer
overdue cases
high-risk schools
escalation queue
6. Parent / Submitter Tracking View (optional)

Simple public status page:

case_id lookup
current status
latest update
Data Model

Create / extend schema:

cases
case_id
case_type
status
priority
assigned_to
created_at
updated_at
due_date
is_urgent
air_quality_case_details
case_id (FK)
submitter_name
submitter_role
email
phone
school_name
building_location
incident_datetime
issue_category
detailed_description
symptoms (json)
affected_count
duration
observations (json)
severity_level
related_incidents
actions_taken
internal_notes
resolution_date
follow_up_date
attachments
id
case_id
file_name
file_type
path
uploaded_at
UX Requirements
Keep current design system
GOV.UK style, clean and accessible
Mobile responsive
Fast loading
Clear badges for severity/status
Do not clutter generic case types
Technical Requirements

Use existing stack and patterns already in the project. Preserve current routes/components where possible. Refactor reusable components instead of duplicating code. Use mock JSON data if backend incomplete.

Demo Data

Generate 10 sample air quality cases with mixed severities and statuses. Include examples such as:

mold in classroom
poor ventilation
chemical smell from lab
temperature too high
dust after maintenance works
Deliverables
Updated dashboard
New create case form
Enhanced case detail page
Seed data
Working filters/search
Clean demo-ready UI
Success Criteria

A judge should be able to open the app and immediately understand that the platform now supports environmental school casework inside the existing caseworker system.