from typing import List, Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class UserInfo:
    unit: Optional[str] = None
    role: Optional[str] = None
    
    def is_complete(self) -> bool:
        return bool(self.unit and self.role)

class HospitalUnits:
    RONALD_REGAN_HOSPITAL = {
        'RR 6N': ['6N', '6 NORTH', 'NEUROSURGERY', 'NEUROLOGY', 'NEURO'],
        'RR 6E': ['6E', '6 EAST', 'ONCOLOGY'],
        'RR 6W': ['6W', '6 WEST', 'NEUROLOGY', 'SURGERY', 'VASCULAR', 'VASCULAR SURGERY', 'PLASTICS', 'PLASTIC SURGERY'],
        'RR 7N': ['7N', '7 NORTH', 'CARDIAC OBSERVATION UNIT', 'CARDIOLOGY', 'COU'],
        'RR 7E': ['7E', '7 EAST', 'GENERAL MEDICINE', 'INTERNAL MEDICINE', 'GENERAL MED', 'MEDICINE'],
        'RR 7W': ['7W', '7 WEST', 'MOU', 'MEDICAL OBERVATION UNIT'],
        'RR 8N': ['8N', '8 NORTH', 'LIVER TRANSPLANT', 'LIVER TX'],
        'RR 8E': ['8E', '8 EAST', 'GENERAL SURGERY', 'SURGERY'],
        'RR 8W': ['8W', '8 WEST', 'UROLOGY', 'HEAD & NECK', 'GENERAL SURGERY', 'SURGERY'],
        'RR 6ICU': ['6ICU', '6 NEUROLOGICAL INTENSIVE CARE UNIT', 'ICU', 'NEUROSURGERY', 'TRAUMA', 'SURGERY'],
        'RR 7ICU': ['7ICU', '7 CARDIAC SURGERY UNIT', 'ICU', 'CARDIOLOGY', 'HEART TRANSPLANT', 'CARDIO-THORACIC', 'VASCULAR', 'SURGERY'],
        'RR 8ICU': ['8ICU', '8 INTENSIVE CARE UNIT', 'ICU', 'LIVER TRANSPLANT', 'SURGERY'],
        'RR 4ICU': ['4ICU', '4 ICU', 'ICU', 'MEDICAL ICU', 'MEDICINE'],
        'RR ED': ['RR ED', 'ED', 'ER', 'EMC', 'EMERGENCY', 'EMERGENCY ROOM'],
    }
    
    SANTA_MONICA_HOSPITAL = {
        'SM 4CWICU': ['4CWICU', '4 CENTRAL WING ICU', 'ICU', 'PICU'],
        'SM ED': ['SM ED', 'ED', 'ER', 'EMC', 'EMERGENCY', 'EMERGENCY ROOM'],
    }
    
    ALL_UNITS = {**RONALD_REGAN_HOSPITAL, **SANTA_MONICA_HOSPITAL}
    
    @classmethod
    def find_unit(cls, user_input: str) -> Optional[str]:
        user_input_upper = user_input.upper()
        
        # Check exact match first
        if user_input_upper in cls.ALL_UNITS:
            return user_input_upper
            
        # Check aliases
        for unit, aliases in cls.ALL_UNITS.items():
            if user_input_upper in [alias.upper() for alias in aliases]:
                return unit
                
        return None

def extract_user_info(message: str, current_info: UserInfo) -> UserInfo:
    """Extract unit and role from user message"""
    message_upper = message.upper()
    new_info = UserInfo(unit=current_info.unit, role=current_info.role)
    
    # Extract role - look for common nursing roles
    roles = ['NURSE', 'DOCTOR', 'PHYSICIAN', 'TECH', 'TECHNICIAN', 'ASSISTANT', 'RN', 'LPN', 'CNA']
    for role in roles:
        if role in message_upper:
            if role in ['RN', 'LPN', 'CNA']:
                new_info.role = 'NURSE'
            else:
                new_info.role = role
            break
    
    # Extract unit - check if any unit keywords are mentioned
    found_unit = HospitalUnits.find_unit(message)
    if found_unit:
        new_info.unit = found_unit
    
    return new_info
