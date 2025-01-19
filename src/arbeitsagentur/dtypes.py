from dataclasses import dataclass


@dataclass
class VacancySearchResponse:
    id: str
    title: str


@dataclass
class SearchResponse:
    total: int
    page: int
    size: int
    result: list[VacancySearchResponse]


@dataclass
class VacancyDetails:
    title: str
    company: str
    address: str
    phone_number: str
    email: str
    url: str


@dataclass
class VacancyFullInfo:
    job_offer_type: str
    job_offer_title: str
    job_offer_description: str
    remote_work: bool
    shift_work_night_weekend: bool
    part_time_evening: bool
    part_time_afternoon: bool
    part_time_morning: bool
    part_time_flexible: bool
    full_time: bool
    entry_period_from: str
    salary: str
    contract_duration: str
    is_minimum_wage_job: bool
    disability_required: bool
    job_locations: list[dict[str, object]]
    is_private_recruitment: bool
    is_employee_leasing: bool
    publication_period_from: str
    modification_date: str
    is_supported: bool
    main_profession: str
    company: str
    employer_customer_number_hash: str
    partner_url: str
    partner_name: str
    reference_number: str
