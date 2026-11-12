def take_damage(hero, damage_amount):
    # Subtract damage_amount from hero["health"] and save it back
    hero["health"] -= damage_amount
    
    # If hero["health"] drops below 0, set it to 0
    if hero["health"] < 0:
        hero["health"] = 0
        
    # Return the updated hero dictionary
    return hero


def heal_until_full(hero, potion_power):
    # Run a loop while hero["health"] is less than 100
    while hero["health"] < 100:
        hero["health"] += potion_power
        
    # If hero["health"] went over 100, cap it at 100
    if hero["health"] > 100:
        hero["health"] = 100
        
    # Return the updated hero dictionary
    return hero
