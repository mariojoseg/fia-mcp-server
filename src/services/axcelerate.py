import os
import json
import logging
import requests
from typing import List, Dict, Optional, Any
from datetime import date, datetime
 
from dotenv import load_dotenv
load_dotenv(override=True)
 
class Axcelerate():
    def __init__(self):
        """
        Initialize Axcelerate API client
        """
        self.base_url = os.getenv('AXCELERATE_BASE_URL')
        self.headers = {
            "wstoken": os.getenv('AXCELERATE_WSTOKEN'),
            "apitoken": os.getenv('AXCELERATE_APITOKEN')
        }

    
    def search_users(
            self,
            q: Optional[str] = None,
            givenName: Optional[str] = None,
            surname: Optional[str] = None,
            emailAddress: Optional[str] = None,
            contactRoleID: Optional[int] = None,
            contactIDs: Optional[List[int]] = None,
            contactID: Optional[int] = None
        ) -> List[Dict[str, Any]]:
        """
        Search for users

        Args:
            q: A search string. i.e q="John Doe"
            givenName: The user's given name. i.e givenName="John"
            surname: The user's surname. i.e surname="Doe"
            emailAddress: The user's email address. i.e emailAddress="john.doe@example.com"
            contactRoleID: The ID of the contact role to filter by. i.e contactRoleID=1
            contactIDs: A list of contact IDs to filter by. i.e contactIDs=[1, 2, 3]
            contactID: A single contact ID to filter by. i.e contactID=1
        """
        url = f"{self.base_url}/contacts/search/"
        params = {
            "q": q,
            "givenName": givenName,
            "surname": surname,
            "emailAddress": emailAddress,
            "contactRoleID": contactRoleID,
            "contactIDs": contactIDs,
            "contactID": contactID
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            users = response.json()

            payload: List[Dict[str, Any]] = []
            for user in users:
                if not isinstance(user, dict):
                    continue
                payload.append({
                    "contact_id": user.get("CONTACTID"),
                    "user_id": user.get("USERID"),
                    "given_name": user.get("GIVENNAME"),
                    "surname": user.get("SURNAME"),
                    "email": user.get("EMAILADDRESS"),
                    "alt_email": user.get("EMAILADDRESSALTERNATIVE"),
                    "sex": user.get("SEX"),
                    "mobile": user.get("MOBILEPHONE"),
                    "work_phone": user.get("WORKPHONE"),
                    "organisation": user.get("ORGANISATION"),
                    "position": user.get("POSITION"),
                    "active": user.get("CONTACTACTIVE"),
                })

            return payload
        except requests.RequestException as e:
            print(f"Error searching user: {e}")
            return []


    def get_courses(
            self,
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
        Retrieve a list of courses.

        Args:
            id: The ID of the Course to filter
            search_term: Search term to filter courses
            type: Type of the course (e.g., 'w' for workshop, 'p' for accredited program, 'el' for e-learning). (default: all)
            training_area: Training area to filter courses. ("FIA Microlearning", "FIA Courses")
            offset: Used for paging - start at record. (default: 0)
            display_length: Used for paging - total records to retrieve. (default: 10)
            sort_column: The column index to sort by. (default: '1')
            sort_direction: The sort by direction 'ASC' OR 'DESC'. (default: 'ASC')
            current: Current courses flag. True to show only current courses. (default: true)
            public: Whether to include public courses only. If false, returns all course types regardless of public settings. (default: true)
            isActive: Whether to include active/inactive courses only. (default: both)

        Returns:
            List of course dictionaries
        """
        url = f"{self.base_url}/courses/"
        params = {
            "id": id,
            "searchTerm": search_term,
            "type": type,
            "trainingArea": 'FIA Courses',
            "offset": offset,
            "displayLength": display_length,
            "sortColumn": sort_column,
            "sortDirection": sort_direction,
            "current": current,
            "public": public,
            "isActive": isActive
        }
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            courses = response.json()
            
            payload: List[Dict[str, Any]] = []
            for course in courses:
                payload.append({
                    "ID": course.get("ID"),
                    "NAME": course.get("NAME"),
                    "STREAMNAME": course.get("STREAMNAME"),
                    "DIPLOMAVERSION": course.get("DIPLOMAVERSION"),
                    "CODE": course.get("CODE"),
                    "GST_TYPE": course.get("GST_TYPE"),
                    "COST": course.get("COST"),
                    "DELIVERY": course.get("DELIVERY"),
                    "DURATION": course.get("DURATION"),
                    "DURATIONTYPE": course.get("DURATIONTYPE"),
                    "ISACTIVE": course.get("ISACTIVE"),
                    "TYPE": course.get("TYPE"),
                    "SHORTDESCRIPTION": course.get("SHORTDESCRIPTION"),
                })
            return payload
        except requests.exceptions.RequestException as e:
            print(f"Error fetching courses: {e}")
            return []


    def get_course_instance(self, course_id: int, type: str) -> List[Dict]:
        """
        Retrieve a list of course instances (cohorts) for a specific course.

        Args:
            course_id: The ID of the course to retrieve instances for.
            type: The type of the course instance (e.g., 'w' for workshop, 'p' for accredited program, 'el' for e-learning).

        Returns:
            A list of course instance dictionaries.
        """
        url = f"{self.base_url}/course/instances"
        params = {"ID": course_id, "type": type}
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching course instances: {e}")
            return []


    def get_recorded_webinars(self) -> List[Dict]:
        """
        Retrieve a list of recorded webinars.

        This function retrieves webinars that have CPD points and are used 
        to help students keep track of their learning journey.

        Returns:
            A list of recommended webinar dictionaries.
        """
        url = f"{self.base_url}/courses/"
        params = {"trainingArea": "FIA Microlearning", "displayLength": 100}
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            webinars = response.json()
            payload = []
            for webinar in webinars:
                payload.append({
                    "ID": webinar.get('ID'),
                    "NAME": webinar.get('NAME'),
                    "STREAMNAME": webinar.get('STREAMNAME'),
                    "DIPLOMAVERSION": webinar.get('DIPLOMAVERSION'),
                    "CODE": webinar.get('CODE'),
                    "GST_TYPE": webinar.get('GST_TYPE'),
                    "COST": webinar.get('COST'),
                    "DELIVERY": webinar.get('DELIVERY'),
                    "DURATION": webinar.get('DURATION'),
                    "DURATIONTYPE": webinar.get('DURATIONTYPE'),
                    "ISACTIVE": webinar.get('ISACTIVE'),
                    "TYPE": webinar.get('TYPE'),
                    "SHORTDESCRIPTION": webinar.get('SHORTDESCRIPTION'),
                })
            return payload
        except Exception as e:
            logging.error(f"Error retrieving webinars: {e}")
            return [{"error": True,"message": f"Unexpected error: {str(e)}"}]


    def search_courses(
            self,
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
        Search for courses based on various parameters.

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
        url = f"{self.base_url}/course/instance/search/"
        params = {
            "id": id,
            "instanceID": instance_id,
            "type": type,
            "trainingCategory": training_category,
            "location": location,
            "state": state,
            "code": code,
            "name": name,
            "searchTerm": search_term,
            "enrolmentOpen": enrolment_open,
            "startDate_min": startDate_min.isoformat() if startDate_min else None,
            "startDate_max": startDate_max.isoformat() if startDate_max else None,
            "finishDate_min": finishDate_min.isoformat() if finishDate_min else None,
            "finishDate_max": finishDate_max.isoformat() if finishDate_max else None,
            "lastUpdated_min": lastUpdated_min.isoformat() if lastUpdated_min else None,
            "lastUpdated_max": lastUpdated_max.isoformat() if lastUpdated_max else None,
            "offset": offset,
            "displayLength": display_length,
            "sortColumn": sort_column,
            "sortDirection": sort_direction,
            "public": public,
            "isActive": isActive,
            "status": status
        }
        try:
            response = requests.post(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                return data.get("data", [])
            elif isinstance(data, list):
                return data
            else:
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error searching courses: {e}")
            return []

    def get_fia_courses(self, display_length: Optional[int] = None) -> List[Dict]:
        """
        Retrieve FIA training courses.

        Args:
            display_length: Used for paging - total records to retrieve. (default is 10)
        Returns:
            List of FIA training course dictionaries
        """
        return self.search_courses(
            type="p",
            training_category="FIA Courses",
            display_length=display_length,
        )
    
    def get_student_enrollments(self, contactID: int) -> Dict[str, Any]:
        """Retrieve enrolment status and list of courses for a specific learner.

        Calls /course/enrolments/ with a contactID filter (if supported by the API)
        and normalises the response into a simple structure.

        Args:
            contactID: The Axcelerate CONTACTID of the learner.

        Returns:
            Dict with keys:
                enrolled: bool - whether the learner has at least one enrolment
                courses: List[Dict] - simplified list of course enrolments with fields:
                    instance_id, enrol_id, learner_id, contact_id, name, code,
                    status, type, enrolment_date, start_date, finish_date
        """
        url = f"{self.base_url}/course/enrolments/"
        params = {"contactID": contactID}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            payload = response.json()

            if isinstance(payload, list):
                enrolments = payload
            elif isinstance(payload, dict):
                enrolments = payload.get("data", [])
            else:
                enrolments = []

            # Filter and transform
            courses: List[Dict[str, Any]] = []
            for e in enrolments:
                if int(e.get("CONTACTID", -1)) != contactID:
                    continue
                courses.append({
                    "instance_id": e.get("INSTANCEID"),
                    "enrol_id": e.get("ENROLID"),
                    "learner_id": e.get("LEARNERID"),
                    "contact_id": e.get("CONTACTID"),
                    "name": e.get("NAME"),
                    "code": e.get("CODE"),
                    "status": e.get("STATUS"),
                    "type": e.get("TYPE"),
                    "enrolment_date": e.get("ENROLMENTDATE"),
                    "start_date": e.get("STARTDATE"),
                    "finish_date": e.get("FINISHDATE"),
                })

            return {"enrolled": len(courses) > 0, "courses": courses}
        except requests.RequestException as exc:
            print(f"Error retrieving enrolments for contactID {contactID}: {exc}")
            return {"enrolled": False, "courses": []}

    def get_course_enrolments(self, instanceID: int) -> List[Dict]:
        """
        Retrieve a simplified list of enrolled students for a specific course instance.

        The raw API returns a list of (program) enrolment objects which contain many
        fields. This method normalises that response to a clean list of student
        records with only the most relevant learner-centric fields.

        Args:
            instanceID: The Axcelerate course instance ID to retrieve enrolments for.

        Returns:
            A list of dictionaries, each representing an enrolled student with keys:
            contact_id, given_name, surname, email, status, enrolment_date,
            finish_date, instance_id, code, enrol_id, learner_id.
        """
        url = f"{self.base_url}/course/enrolments/"
        params = {"instanceID": instanceID}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            payload = response.json()

            # Normalise to a list of enrolment dicts
            if isinstance(payload, list):
                enrolments = payload
            elif isinstance(payload, dict):
                enrolments = payload.get("data", [])
            else:
                enrolments = []

            students: List[Dict[str, Any]] = []
            for e in enrolments:
                # Filter strictly by instance (defensive: API should already filter)
                if int(e.get("INSTANCEID", -1)) != instanceID:
                    continue
                students.append({
                    "contact_id": e.get("CONTACTID"),
                    "given_name": e.get("GIVENNAME"),
                    "surname": e.get("SURNAME"),
                    "email": e.get("EMAIL"),
                    "status": e.get("STATUS"),
                    "enrolment_date": e.get("ENROLMENTDATE"),
                    "finish_date": e.get("FINISHDATE"),
                    "instance_id": e.get("INSTANCEID"),
                    "code": e.get("CODE"),
                    "enrol_id": e.get("ENROLID"),
                    "learner_id": e.get("LEARNERID"),
                })

            return students
        except requests.RequestException as exc:
            print(f"Error retrieving enrolments for instanceID {instanceID}: {exc}")
            return []


if __name__ == "__main__":
    ax = Axcelerate()

    # DEMO: SEARCH USER
    # user_search_results = ax.search_users(q="Mario", surname="Garbo")
    # print("User search results:", json.dumps(user_search_results, indent=2))
    
    # DEMO: SEARCH COURSE
    # search_results = ax.search_courses(name="Accredited chief warden training")
    # print("Search results:", json.dumps(search_results, indent=2))
    
    # DEMO: RECORDED WEBINARS
    # recorded_webinars = ax.get_recorded_webinars()
    # print(json.dumps(recorded_webinars, indent=2))

    # DEMO: GET FIA COURSES
    # fia_courses = ax.get_fia_courses()
    # print("FIA courses:", json.dumps(fia_courses, indent=2))

    # DEMO: GET COURSE INSTANCE
    # course_instance = ax.get_course_instance(course_id=77281, type="p")
    # print("Course instance details:", json.dumps(course_instance, indent=2))

    # DEMO: STUDENT ENROLMENTS
    # student_result = ax.get_student_enrollments(contactID=14107956)
    # print("Student enrolments:", student_result)

    # DEMO: ENROLMENTS FOR A COURSE INSTANCE
    # course_students = ax.get_course_enrolments(instanceID=1756323)
    # print("Course instance enrolments (simplified):", course_students)