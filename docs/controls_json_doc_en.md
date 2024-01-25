# Amazon S3 Security Baseline Documentation

This document describes the structure of the JSON used to define a security baseline for resources stored in Amazon S3. The JSON comprises a list of security controls, each detailing a specific recommended practice for ensuring the security of data stored in S3.

## JSON Structure

The JSON is structured as an object containing a single key `SecurityControlsAmazonS3`, which maps to a list of security controls. Each security control is an object that describes a specific security practice.

### Fields for Each Security Control

Each security control includes the following fields:

- `SecurityDomain`: Describes the security area that the control pertains to (e.g., "Identity and Access Management", "Encryption").
- `ControlType`: Indicates whether the control is an access control, technical control, etc.
- `Control`: The name of the security control (e.g., "Bucket Policies", "Encryption at Rest and in Transit").
- `Description`: A detailed description of the control, explaining its purpose and importance for the security of Amazon S3.
- `DependsOnCompanyPolicies`: Indicates whether the implementation of the control depends on specific policies and definitions of the company (`Yes`) or if it is a standard practice that can be universally applied (`No`).

### Example of a Security Control

```json
{
  "SecurityDomain": "Identity and Access Management",
  "ControlType": "Access Control",
  "Control": "Bucket Policies",
  "Description": "Define restrictive bucket policies following the principle of least privilege, allowing access only to necessary entities.",
  "DependsOnCompanyPolicies": "Yes"
}
