from dataclasses import dataclass


@dataclass(frozen=True)
class CityBaseline:
    code: str
    city: str
    state: str
    latitude: float
    longitude: float
    population_millions: float
    unemployment_rate: float
    inflation_rate: float
    crime_rate: float
    poverty_rate: float
    population_density: float


TOP_50_CITIES: list[CityBaseline] = [
    CityBaseline("IN-MUM", "Mumbai", "Maharashtra", 19.0760, 72.8777, 20.96, 7.8, 5.7, 68, 13, 21000),
    CityBaseline("IN-DEL", "Delhi", "Delhi", 28.6139, 77.2090, 32.94, 8.4, 6.2, 72, 10, 11320),
    CityBaseline("IN-BLR", "Bengaluru", "Karnataka", 12.9716, 77.5946, 13.61, 5.6, 4.8, 51, 9, 4381),
    CityBaseline("IN-HYD", "Hyderabad", "Telangana", 17.3850, 78.4867, 10.80, 6.1, 5.3, 55, 11, 18500),
    CityBaseline("IN-AMD", "Ahmedabad", "Gujarat", 23.0225, 72.5714, 8.65, 5.9, 5.6, 49, 12, 11895),
    CityBaseline("IN-CHE", "Chennai", "Tamil Nadu", 13.0827, 80.2707, 11.78, 5.1, 5.2, 48, 8, 26553),
    CityBaseline("IN-KOL", "Kolkata", "West Bengal", 22.5726, 88.3639, 15.33, 6.9, 5.9, 57, 15, 24252),
    CityBaseline("IN-SUR", "Surat", "Gujarat", 21.1702, 72.8311, 7.78, 5.7, 5.4, 46, 10, 13700),
    CityBaseline("IN-PUN", "Pune", "Maharashtra", 18.5204, 73.8567, 7.17, 6.3, 5.5, 54, 11, 5600),
    CityBaseline("IN-JAI", "Jaipur", "Rajasthan", 26.9124, 75.7873, 4.11, 10.4, 7.3, 64, 18, 6500),
    CityBaseline("IN-LKO", "Lucknow", "Uttar Pradesh", 26.8467, 80.9462, 3.95, 8.9, 6.6, 62, 20, 6900),
    CityBaseline("IN-KAN", "Kanpur", "Uttar Pradesh", 26.4499, 80.3319, 3.20, 9.2, 6.7, 67, 21, 6900),
    CityBaseline("IN-NAG", "Nagpur", "Maharashtra", 21.1458, 79.0882, 3.05, 7.1, 5.9, 58, 14, 11500),
    CityBaseline("IN-IND", "Indore", "Madhya Pradesh", 22.7196, 75.8577, 3.28, 7.6, 6.1, 56, 17, 10600),
    CityBaseline("IN-THA", "Thane", "Maharashtra", 19.2183, 72.9781, 2.62, 7.4, 5.8, 52, 12, 13000),
    CityBaseline("IN-BHO", "Bhopal", "Madhya Pradesh", 23.2599, 77.4126, 2.56, 7.9, 6.0, 59, 17, 8550),
    CityBaseline("IN-VIS", "Visakhapatnam", "Andhra Pradesh", 17.6868, 83.2185, 2.39, 6.7, 5.7, 45, 12, 7600),
    CityBaseline("IN-PAT", "Patna", "Bihar", 25.5941, 85.1376, 2.58, 12.6, 7.9, 76, 28, 1823),
    CityBaseline("IN-VAD", "Vadodara", "Gujarat", 22.3072, 73.1812, 2.19, 5.8, 5.4, 47, 11, 9500),
    CityBaseline("IN-GHA", "Ghaziabad", "Uttar Pradesh", 28.6692, 77.4538, 2.73, 8.7, 6.5, 70, 18, 8300),
    CityBaseline("IN-LUD", "Ludhiana", "Punjab", 30.9010, 75.8573, 2.15, 7.2, 6.0, 60, 12, 8700),
    CityBaseline("IN-AGR", "Agra", "Uttar Pradesh", 27.1767, 78.0081, 2.26, 8.3, 6.4, 63, 19, 10800),
    CityBaseline("IN-NAS", "Nashik", "Maharashtra", 19.9975, 73.7898, 2.12, 6.8, 5.8, 50, 14, 5600),
    CityBaseline("IN-FAR", "Faridabad", "Haryana", 28.4089, 77.3178, 1.96, 8.0, 6.1, 66, 13, 9100),
    CityBaseline("IN-MEE", "Meerut", "Uttar Pradesh", 28.9845, 77.7064, 1.87, 8.8, 6.7, 69, 20, 8900),
    CityBaseline("IN-RAJ", "Rajkot", "Gujarat", 22.3039, 70.8022, 1.93, 5.9, 5.5, 44, 10, 8500),
    CityBaseline("IN-KAL", "Kalyan-Dombivli", "Maharashtra", 19.2403, 73.1305, 1.80, 7.4, 5.9, 54, 13, 14700),
    CityBaseline("IN-VAS", "Vasai-Virar", "Maharashtra", 19.3919, 72.8397, 1.63, 7.5, 5.8, 55, 14, 13600),
    CityBaseline("IN-VAR", "Varanasi", "Uttar Pradesh", 25.3176, 82.9739, 1.70, 8.6, 6.5, 61, 21, 7300),
    CityBaseline("IN-SRI", "Srinagar", "Jammu and Kashmir", 34.0837, 74.7973, 1.59, 9.6, 6.7, 58, 16, 4100),
    CityBaseline("IN-AUR", "Aurangabad", "Maharashtra", 19.8762, 75.3433, 1.57, 7.0, 5.9, 49, 15, 8200),
    CityBaseline("IN-DHA", "Dhanbad", "Jharkhand", 23.7957, 86.4304, 1.53, 9.3, 6.8, 65, 24, 6000),
    CityBaseline("IN-AMR", "Amritsar", "Punjab", 31.6340, 74.8723, 1.48, 7.4, 6.2, 59, 14, 6400),
    CityBaseline("IN-NAV", "Navi Mumbai", "Maharashtra", 19.0330, 73.0297, 1.53, 6.9, 5.6, 46, 9, 10300),
    CityBaseline("IN-ALL", "Prayagraj", "Uttar Pradesh", 25.4358, 81.8463, 1.54, 8.5, 6.4, 60, 21, 6500),
    CityBaseline("IN-RAN", "Ranchi", "Jharkhand", 23.3441, 85.3096, 1.46, 8.8, 6.5, 62, 22, 6100),
    CityBaseline("IN-HOW", "Howrah", "West Bengal", 22.5958, 88.2636, 1.40, 7.1, 6.0, 58, 16, 21000),
    CityBaseline("IN-COI", "Coimbatore", "Tamil Nadu", 11.0168, 76.9558, 2.14, 5.3, 5.1, 42, 9, 7500),
    CityBaseline("IN-JAB", "Jabalpur", "Madhya Pradesh", 23.1815, 79.9864, 1.27, 7.8, 6.2, 57, 18, 5600),
    CityBaseline("IN-GWA", "Gwalior", "Madhya Pradesh", 26.2183, 78.1828, 1.38, 8.1, 6.3, 61, 19, 5200),
    CityBaseline("IN-VIJ", "Vijayawada", "Andhra Pradesh", 16.5062, 80.6480, 1.48, 6.5, 5.7, 48, 13, 10400),
    CityBaseline("IN-JOD", "Jodhpur", "Rajasthan", 26.2389, 73.0243, 1.38, 9.9, 7.2, 60, 17, 5300),
    CityBaseline("IN-MAD", "Madurai", "Tamil Nadu", 9.9252, 78.1198, 1.46, 5.5, 5.2, 45, 10, 6800),
    CityBaseline("IN-RAI", "Raipur", "Chhattisgarh", 21.2514, 81.6296, 1.42, 7.7, 6.1, 58, 19, 5200),
    CityBaseline("IN-KOT", "Kota", "Rajasthan", 25.2138, 75.8648, 1.25, 9.4, 7.0, 57, 16, 4100),
    CityBaseline("IN-GUW", "Guwahati", "Assam", 26.1445, 91.7362, 1.25, 7.2, 5.6, 59, 19, 2010),
    CityBaseline("IN-CHA", "Chandigarh", "Chandigarh", 30.7333, 76.7794, 1.19, 6.2, 5.8, 50, 8, 9258),
    CityBaseline("IN-SOL", "Solapur", "Maharashtra", 17.6599, 75.9064, 1.18, 7.3, 6.0, 52, 16, 7100),
    CityBaseline("IN-HUB", "Hubballi-Dharwad", "Karnataka", 15.3647, 75.1240, 1.17, 6.1, 5.4, 47, 12, 4600),
    CityBaseline("IN-MYS", "Mysuru", "Karnataka", 12.2958, 76.6394, 1.24, 5.8, 5.2, 43, 10, 6800),
]

CITY_BY_CODE = {city.code: city for city in TOP_50_CITIES}
