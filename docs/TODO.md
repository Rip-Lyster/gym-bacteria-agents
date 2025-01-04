# Training System TODO List

## MVP (Weekend Project)
### Day 1: Core Setup
- [ ] Database Essentials
  - [ ] Set up NeonDB in Vercel
  - [ ] Add database URLs to environment
  - [ ] Basic schema:
    - [ ] Users (id, access_key, nickname)
    - [ ] Training Plans (id, user_id, name, start_date, end_date)
    - [ ] Exercise Types (id, name, category, parameters)
    - [ ] Workouts (id, name, planned_date, status)
  - [ ] Initial migration with indexes
  - [ ] Add sample exercise types

- [ ] Basic Backend
  - [ ] SQLAlchemy models
  - [ ] Essential endpoints:
    - [ ] User creation/access
    - [ ] Training plan CRUD
    - [ ] Workout management
    - [ ] Exercise type listing

### Day 2: UI Implementation
- [ ] Essential Frontend
  - [ ] User access screen
  - [ ] Training plan creation/view
  - [ ] Workout scheduler
  - [ ] Basic exercise logger
- [ ] Test end-to-end flow

## Future Development

### Database Enhancements
- [ ] Add remaining tables
  - [ ] Training blocks
  - [ ] Workout exercises
  - [ ] Exercise logs
- [ ] Add advanced fields
  - [ ] Progression tracking
  - [ ] Weekly targets
  - [ ] Detailed exercise parameters
- [ ] Optimize indexes
- [ ] Add data validation

### Backend Improvements
- [ ] Full API implementation
  - [ ] Training block management
  - [ ] Exercise logging
  - [ ] Progress tracking
- [ ] Add authentication
- [ ] Add API documentation

### Frontend Features
- [ ] Advanced UI components
  - [ ] Training block designer
  - [ ] Progress graphs
  - [ ] Exercise history
- [ ] State management
- [ ] Real-time updates

### Development Tools
- [ ] Testing infrastructure
- [ ] CI/CD pipeline
- [ ] Development environment

### Monitoring & Optimization
- [ ] Performance monitoring
- [ ] Query optimization
- [ ] Usage analytics

---
Note: MVP focuses on core training plan and workout management. Additional features will be added based on user feedback. 