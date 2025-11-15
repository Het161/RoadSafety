# 🚗 RoadSafeCost AI - Road Safety Intervention Cost Estimator

**National Road Safety Hackathon 2025 - Problem Statement 1.1**  
*Organized by Centre of Excellence for Road Safety (CoERS), RBG Labs, IIT Madras*

## 📋 Problem Statement
Development of Estimator Tool for Intervention - An AI application that automatically estimates material-only costs for road safety interventions by extracting specifications from IRC standards and fetching current prices from official sources.

## 💡 Solution Overview
RoadSafeCost AI automates the manual process of cost estimation for road safety interventions recommended in audit reports. The tool extracts intervention details, maps them to IRC standards, calculates material quantities, and produces transparent, itemized cost estimates with full traceability.

## ✨ Key Features
- **IRC-Compliant**: Integrates IRC-67, IRC-99, and IRC-SP:87 specifications
- **Official Rate Sources**: Fetches material rates from CPWD SOR and GeM portal
- **Explainability**: Every cost line item includes IRC clause reference and rate source
- **Accuracy**: Designed to stay within 10% tolerance band
- **Material-Only Costing**: Excludes labor, installation, and taxes as required

## 🏗️ Architecture
- **Backend**: FastAPI (Python 3.9+)
- **Database**: SQLite
- **Data Validation**: Pydantic models
- **Standards**: IRC-67-2022, IRC-99-2018, IRC-SP:87-2020

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

