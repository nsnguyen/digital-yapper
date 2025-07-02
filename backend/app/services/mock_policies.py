ICU_POLICIES = {
    "hand_hygiene": {
        "title": "Hand Hygiene Protocol for ICU",
        "content": """
**Hand Hygiene in ICU Settings**

1. **Before patient contact**: Use alcohol-based hand rub for 15-20 seconds
2. **After patient contact**: Wash hands with soap and water for 20 seconds
3. **Before invasive procedures**: Surgical hand antisepsis required
4. **After contact with contaminated surfaces**: Immediate hand hygiene

**ICU-Specific Requirements:**
- Hand hygiene compliance must be >95% in ICU settings
- Use chlorhexidine-based products for high-risk patients
- Gloving does not replace hand hygiene

**Monitoring:** Hand hygiene compliance is monitored hourly in ICU units.
        """
    },
    "iv_lines": {
        "title": "IV Line Management in ICU",
        "content": """
**IV Line Care and Maintenance**

1. **Assessment frequency**: Every 4 hours minimum
2. **Site inspection**: Check for signs of infiltration, phlebitis, infection
3. **Dressing changes**: Transparent dressings every 7 days or when compromised
4. **Flushing protocol**: Normal saline flush before and after medication administration

**ICU-Specific Guidelines:**
- Central lines require daily necessity assessment
- Use chlorhexidine for skin antisepsis
- Document all assessments in ICU flowsheet

**Removal criteria:** Remove peripheral IVs after 72-96 hours unless clinically indicated.
        """
    },
    "isolation_precautions": {
        "title": "Isolation Precautions in ICU",
        "content": """
**ICU Isolation Protocols**

1. **Standard precautions**: Apply to all patients
2. **Contact precautions**: MRSA, VRE, C. diff patients
3. **Droplet precautions**: Respiratory infections
4. **Airborne precautions**: TB, COVID-19 (negative pressure rooms)

**ICU Requirements:**
- PPE donning/doffing stations outside each room
- Dedicated equipment for isolated patients
- Enhanced environmental cleaning protocols

**Documentation:** All isolation measures documented in ICU assessment forms.
        """
    }
}

ED_POLICIES = {
    "triage": {
        "title": "Emergency Department Triage Protocol",
        "content": """
**ED Triage Assessment**

1. **ESI Level 1**: Immediate life-threatening conditions
2. **ESI Level 2**: High-risk situations, should be seen within 14 minutes
3. **ESI Level 3**: Stable patients requiring multiple resources
4. **ESI Level 4**: Stable patients requiring one resource
5. **ESI Level 5**: Non-urgent conditions

**ED-Specific Requirements:**
- Triage completed within 10 minutes of arrival
- Vital signs for all patients except ESI 5
- Pain assessment using 0-10 scale

**Documentation:** All triage decisions documented in ED tracking system.
        """
    },
    "hand_hygiene": {
        "title": "Hand Hygiene in Emergency Department",
        "content": """
**ED Hand Hygiene Protocol**

1. **Between patients**: Alcohol-based hand rub minimum
2. **After contact with blood/body fluids**: Soap and water required
3. **Before procedures**: Enhanced hand hygiene with antiseptic
4. **High-turnover environment**: Hand hygiene stations every 10 feet

**ED-Specific Challenges:**
- Rapid patient turnover requires efficient hand hygiene
- Emergency situations may require modified protocols
- Use of gloves common but doesn't replace hand hygiene

**Compliance target:** >90% in ED (lower than ICU due to emergency nature).
        """
    },
    "medication_administration": {
        "title": "Emergency Medication Administration",
        "content": """
**ED Medication Safety**

1. **Verification**: Two patient identifiers before any medication
2. **High-alert medications**: Double verification required
3. **Emergency situations**: Verbal orders acceptable with immediate documentation
4. **Pain management**: Follow ED pain protocols

**ED-Specific Protocols:**
- Crash cart medications have special procedures
- Conscious sedation requires continuous monitoring
- Allergy verification critical in emergency settings

**Documentation:** All medications documented within 30 minutes in ED system.
        """
    }
}

def get_mock_policies(unit: str, query: str) -> list[dict[str, str]]:
    """Return mock policies based on unit and query"""
    
    # Determine which policy set to use
    if 'ICU' in unit.upper():
        policies = ICU_POLICIES
    elif 'ED' in unit.upper() or 'EMERGENCY' in unit.upper():
        policies = ED_POLICIES
    else:
        # Default to ICU policies for other units
        policies = ICU_POLICIES
    
    # Simple keyword matching
    query_lower = query.lower()
    relevant_policies = []
    
    for policy_id, policy_data in policies.items():
        if (policy_id in query_lower or 
            any(keyword in query_lower for keyword in policy_id.split('_')) or
            any(keyword in policy_data['content'].lower() for keyword in query_lower.split()[:3])):
            relevant_policies.append({
                "title": policy_data["title"],
                "content": policy_data["content"],
                "unit_specific": f"This policy is specific to {unit} operations."
            })
    
    # If no specific match, return a general policy
    if not relevant_policies and policies:
        first_policy = list(policies.values())[0]
        relevant_policies.append({
            "title": f"General {unit} Policy",
            "content": first_policy["content"],
            "unit_specific": f"This is a general policy for {unit}. Please be more specific for targeted policies."
        })
    
    return relevant_policies
