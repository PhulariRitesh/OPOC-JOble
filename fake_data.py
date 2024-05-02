import random
from faker import Faker


def generate_sample_data():
    fake = Faker()
    sample_data = {
        "title": "Software Engineer",
        "company": fake.company(),
        "experience": f"{random.randint(1, 10)} years",
        "description": fake.text(),
        "job_link": fake.url(),
        "location": fake.address(),
        "date": str(fake.date_between(start_date='-1y', end_date='today')),
        "salary": f"{random.randint(50000, 200000)} - {random.randint(200000, 300000)} USD",
        "company_link": fake.url(),
        "education": random.choice(["Bachelor's degree", "Master's degree", "PhD"]),
        "employment_type": random.choice(["Full-time", "Part-time", "Contract"]),
        "role": "Software Engineer",
        "skills": random.sample(["python", "java", "c++", "javascript", "ruby", "go", "rust"], k=3),
        "jobid": fake.unique.random_number(digits=5),
    }
    return sample_data


if __name__ == "__main__":
    print(generate_sample_data())