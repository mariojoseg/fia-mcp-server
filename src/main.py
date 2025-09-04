from fastmcp import FastMCP
from src.services.axcelerate import Axcelerate
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import List, Dict, Optional, Any
from datetime import date, datetime

# Initialize the MCP server
fia_mcp = FastMCP(name="FIA MCP Server", version="1.0", auth=None)

# Provide details about the service
@fia_mcp.custom_route("/", methods=["GET"])
async def service_info(request: Request) -> JSONResponse:
    return JSONResponse(
        {"service": "FIA MCP Server", "status": "running", "version": "1.0"}
    )

# Health check endpoint
@fia_mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "healthy", "service": "FIA MCP Server"})


# Initialize the Axcelerate
ax = Axcelerate()

@fia_mcp.tool()
def search_user(
        q: Optional[str] = None,
        givenName: Optional[str] = None,
        surname: Optional[str] = None,
        emailAddress: Optional[str] = None,
        contactRoleID: Optional[int] = None,
        contactIDs: Optional[List[int]] = None,
        contactID: Optional[int] = None
    ) -> List[Dict]:
    """
    Use this tool to search for a users, students, trainers.

    Args:
        q: A search string. i.e q="John Doe"
        givenName: The user's given name. i.e givenName="John"
        surname: The user's surname. i.e surname="Doe"
        emailAddress: The user's email address. i.e emailAddress="john.doe@example.com"
        contactRoleID: The ID of the contact role to filter by. i.e contactRoleID=1
        contactIDs: A list of contact IDs to filter by. i.e contactIDs=[1, 2, 3]
        contactID: A single contact ID to filter by. i.e contactID=1
    
    Returns:
        A list of user dictionaries.
    """
    return ax.search_users(
        q=q,
        givenName=givenName,
        surname=surname,
        emailAddress=emailAddress,
        contactRoleID=contactRoleID,
        contactIDs=contactIDs,
        contactID=contactID
    )


@fia_mcp.tool()
def get_courses(
        id: Optional[int] = None,
        search_term: Optional[str] = None,
        type: Optional[str] = None,
        offset: Optional[int] = None,
        display_length: Optional[int] = None,
        sort_column: Optional[str] = None,
        sort_direction: Optional[str] = None,
        current: Optional[bool] = None,
        public: Optional[bool] = None,
        isActive: Optional[bool] = None,
    ) -> List[Dict]:
    """
    Use this tool to retrieve a list of courses.

    Args:
        id: The ID of the Course to filter
        search_term: Search term to filter courses
        type: Type of the course (e.g., 'w' for workshop, 'p' for accredited program, 'el' for e-learning)
        training_area: Training area to filter courses
        offset: Used for paging - start at record. (default is 0)
        display_length: Used for paging - total records to retrieve. (default is 10)
        sort_column: The column index to sort by. (default is '1')
        sort_direction: The sort by direction 'ASC' OR 'DESC'. (default is 'ASC')
        current: Current courses flag. True to show only current courses
        public: Whether to include public courses only. If false, returns all course types regardless of public settings.
        lastUpdated_min: In 'YYYY-MM-DD hh:mm' format. The course last updated date must be greater than or equal to this datetime. Courses last updated prior to Nov 2018 may not appear. Time is optional and in client's current timezone. Only applicable to w or p types.
        lastUpdated_max: In 'YYYY-MM-DD hh:mm' format. The course last updated date must be less than or equal to this datetime. Courses last updated prior to Nov 2018 may not appear. Time is optional and in client's current timezone. Only applicable to w or p types.
        isActive: Whether to include active/inactive courses only. By default both will be included

    Returns:
        List of all course dictionaries.
    """
    return ax.get_courses(
        id=id,
        search_term=search_term,
        type=type,
        offset=offset,
        display_length=display_length,
        sort_column=sort_column,
        sort_direction=sort_direction,
        current=current,
        public=public,
        isActive=isActive
    )


@fia_mcp.tool()
def get_cohorts(course_id: int, type: str) -> List[Dict[str, Any]]:
    """
    Use this tool to retrieve a cohorts from specific course.

    Args:
        course_id (int): The ID of the course instance to retrieve.
        type (str): The type of the course instance. 'w' for workshop, 'p' for accredited program, 'el' for e-learning.

    Returns:
        A list of dictionaries, each representing a course instance with its details.
    """
    return ax.get_course_instance(course_id=course_id, type=type)


@fia_mcp.tool()
def get_recorded_webinars() -> List[Dict[str, Any]]:
    """
    Use this tool to retrieve a list of recorded webinars.

    This tool retrieves recorded webinars that have CPD points and are used
    to help students keep track of their learning journey.
    Make sure to recommend relevant courses.

    Returns:
        A list of dictionaries, each representing a webinar with its details.
    """
    return ax.get_recorded_webinars()


@fia_mcp.tool()
def search_cohorts(
    id: Optional[int] = None,
    instance_id: Optional[int] = None,
    type: Optional[str] = None,
    training_category: Optional[str] = None,
    location: Optional[str] = None,
    state: Optional[str] = None,
    code: Optional[str] = None,
    name: Optional[str] = None,
    search_term: Optional[str] = None,
    enrolment_open: Optional[bool] = None,
    startDate_min: Optional[date] = None,
    startDate_max: Optional[date] = None,
    finishDate_min: Optional[date] = None,
    finishDate_max: Optional[date] = None,
    lastUpdated_min: Optional[datetime] = None,
    lastUpdated_max: Optional[datetime] = None,
    offset: Optional[int] = None,
    display_length: Optional[int] = None,
    sort_column: Optional[str] = None,
    sort_direction: Optional[str] = None,
    public: Optional[bool] = None,
    isActive: Optional[bool] = None,
    status: Optional[str] = None
) -> List[Dict]:
    """
    Use this tool to search for courses based on various criteria.

   Args:
        id: Activity Type ID
        instance_id: Instance ID
        type: Type of the activity. w = workshop, p = accredited program, el = e-learning, all = workshops, accredited programs and e-learning.
        training_category: Training category
        location: Location of the course
        state: State of the course
        code: Course code
        name: Course name
        search_term: For a general search use this param
        enrolment_open: Whether enrolment is open
        startDate_min: Minimum start date
        startDate_max: Maximum start date
        finishDate_min: Minimum finish date
        finishDate_max: Maximum finish date
        lastUpdated_min: Minimum last updated date
        lastUpdated_max: Maximum last updated date
        offset: Used for paging - start at record. (default is 0)
        display_length: Used for paging - total records to retrieve. (default is 10)
        sort_column: The column index to sort by. (default is '1')
        sort_direction: The sort by direction 'ASC' OR 'DESC'. (default is 'ASC')
        public: Whether to include public courses. If false, returns only In-House course instances. (default is 'true')
        isActive: You can chose to include or exclude Deleted / Archived and Inactive courses.
        status: Status of the Workshop. The available choices are as follows: Active, Cancelled, Completed, Incomplete, Tentative
    Returns:
        List of course dictionaries matching the search criteria
    """
    
    return ax.search_courses(
        id=id,
        instance_id=instance_id,
        type=type,
        training_category=training_category,
        location=location,
        state=state,
        code=code,
        name=name,
        search_term=search_term,
        enrolment_open=enrolment_open,
        startDate_min=startDate_min,
        startDate_max=startDate_max,
        finishDate_min=finishDate_min,
        finishDate_max=finishDate_max,
        lastUpdated_min=lastUpdated_min,
        lastUpdated_max=lastUpdated_max,
        offset=offset,
        display_length=display_length,
        sort_column=sort_column,
        sort_direction=sort_direction,
        public=public,
        isActive=isActive,
        status=status
    )


@fia_mcp.tool()
def get_student_enrollments(contactID: int) -> Dict[str, Any]:
    """
    Use this tool to get all enrolments for a specific student.

    Args:
        contactID (int): ID of the student/user.

    Returns:
        List[Dict]: A list of enrolment dictionaries.
    """
    return ax.get_student_enrollments(contactID)


@fia_mcp.tool()
def get_course_enrolments(instanceID: int) -> List[Dict]:
    """
    Use this tool to get all enrolments for a specific course instance.

    Args:
        instanceID (int): ID of the course instance.

    Returns:
        List[Dict]: A list of enrolment dictionaries.
    """
    return ax.get_course_enrolments(instanceID)


def main():
    """Main entry point for the MCP server."""
    fia_mcp.run(transport='streamable-http', host='0.0.0.0', port=8080)


if __name__ == "__main__":
    main()