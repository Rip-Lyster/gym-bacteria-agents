# Exercise Parameters Guide

This guide explains the parameters used to track exercises in the Gym Bacteria system.

## RPE (Rate of Perceived Exertion)

RPE is a scale used to measure the intensity of an exercise based on how hard it feels to the athlete. It's a subjective measure that helps autoregulate training intensity.

### RPE Scale (1-10)
- **10**: Maximum effort, could not do more reps
- **9**: Could maybe do 1 more rep
- **8**: Could definitely do 1 more rep, maybe 2
- **7**: Could do 2-3 more reps
- **6**: Could do 4-5 more reps
- **5**: Could do 6+ more reps
- **1-4**: Very light, warm-up intensity

### Benefits of Using RPE
1. **Autoregulation**: Allows adjustment based on daily readiness
2. **Progressive Overload**: Helps manage intensity progression
3. **Fatigue Management**: Provides feedback about recovery status
4. **Long-term Development**: Helps athletes learn to gauge effort

## Exercise Parameters

In our JSON exercise structure:

```json
{
    "exercise_type_id": 1,
    "name": "Squat",
    "sequence": 1,
    "planned": {
        "sets": 4,
        "reps": 10,
        "rpe": 7,
        "rest_minutes": 2
    }
}
```

### Parameter Definitions

1. **sets**: Number of sets to perform
   - Type: Integer
   - Example: 4 sets

2. **reps**: Number of repetitions per set
   - Type: Integer or String (for ranges)
   - Examples: 
     - `10` (fixed reps)
     - `"5-5-5"` (different reps per set)

3. **rpe**: Rate of Perceived Exertion
   - Type: Integer (1-10)
   - Example: 7 (could do 2-3 more reps)

4. **rest_minutes**: Rest period between sets
   - Type: Integer
   - Example: 2 (minutes)

## Usage in Training Blocks

Different training blocks typically use different RPE ranges:

### Hypertrophy Block
- RPE: 7-8
- Higher reps (8-12)
- Moderate rest (1-2 minutes)

### Strength Block
- RPE: 8-9
- Lower reps (3-6)
- Longer rest (2-3 minutes)

### Peak Block
- RPE: 9-10
- Very low reps (1-3)
- Full recovery rest (3-5 minutes)

## Implementation Notes

1. **Logging**
   - Actual performance should include achieved RPE
   - Compare planned vs actual RPE for progression

2. **Programming**
   - Start with lower RPE early in training blocks
   - Progress RPE throughout the block
   - Deload by reducing RPE and/or volume

3. **Data Analysis**
   - Track RPE trends over time
   - Use RPE to identify readiness patterns
   - Compare RPE across different exercises

## Related Files
- `api/scripts/populate_dev_db.py` - Sample exercise data
- `api/core/models.py` - Exercise data structure
- `api/routes/workouts.py` - Exercise logging endpoints 