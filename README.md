# 🚗 ESmini Regression Framework

This project provides a Docker-based regression testing framework for [ESmini](https://github.com/esmini/esmini), a lightweight OpenSCENARIO simulation engine. It allows you to define test scenarios in JSON, run them automatically using ESmini, and analyze the results — either locally, in Jenkins, or in Kubernetes.

---

## 📦 Features

- ✅ Run ESmini simulations headlessly from command-line or CI
- ✅ Define test cases using simple JSON config files
- ✅ Automatically verify expected simulation outcomes (e.g. "no collision")
- ✅ Collect logs for review
- ✅ Supports Docker, Jenkins, and Kubernetes

---

## 🗂️ Project Structure

esmini-regressions/
├── configs/ # JSON test configurations
│ ├── regression_highway.json
│ └── regression_overtake.json
├── scenarios/ # OpenSCENARIO (.xosc) test scenarios
│ ├── highway_cut_in.xosc
│ └── overtake_lane_change.xosc
├── logs/ # Simulation logs (auto-generated)
├── regression.py # Main test runner script
├── Dockerfile # Builds ESmini + runner environment
└── Jenkinsfile # Jenkins pipeline definition

---

## ⚙️ Requirements

- Docker (for local or CI use)
- Python 3.x (if running locally without Docker)

---

## 🚀 Quick Start

### 1. Build the Docker Image

```bash
docker build -t esmini-regression .

This pulls the official ESmini binary and sets up the test runner.

2. Run a Regression Test

Example using Docker:

docker run --rm -v $(pwd):/workspace esmini-regression --config configs/regression_highway.json


This runs the scenario defined in configs/regression_highway.json and saves output logs in /logs.

🧪 Writing a Test Case

Each test config is a JSON file like this:

{
  "scenario": "highway_cut_in.xosc",
  "duration": 30,
  "expected_result": "no_collision",
  "log_level": "info"
}


Place your .xosc scenario files in the scenarios/ folder.

🛠️ Running in Jenkins

Jenkinsfile provided for a simple pipeline.

Parameters let you choose which test config to run.

Logs are archived for post-run review.

Make sure the Jenkins agent has Docker access (or uses a Docker-based agent).

☁️ (Optional) Run in Kubernetes

Build & push the Docker image to a container registry.

Use a Kubernetes Job to run the image with a specific config.

Logs can be collected with kubectl logs.

A sample Kubernetes job YAML can be provided on request.

🧹 Cleaning Up

To clean logs:

rm -rf logs/

📌 Notes

ESmini binary is downloaded from the official release:
https://github.com/esmini/esmini/releases

The regression runner uses headless mode and parses stdout for simple validation logic.

Extend the runner to support richer assertions as needed.

🙌 Contributions

Issues, improvements, and pull requests are welcome!
Feel free to fork or clone and adapt to your projects.

📄 License

This project is open source and available under the MIT License.


You can now save this as README.md in the root of your esmini-regressions folder, commit it, and push it to GitHub. Let me know if you'd like a version with build badges, DockerHub links, or contribution guidelines added.
