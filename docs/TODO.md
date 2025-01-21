# Training System TODO List

## MVP (Weekend Project)
### Day 1: Core Setup ✅
- [x] Database Essentials
  - [x] Set up NeonDB in Vercel
  - [x] Add database URLs to environment
  - [x] Basic schema:
    - [x] Users (id, access_key, nickname)
    - [x] Training Plans (id, user_id, name, start_date, end_date)
    - [x] Exercise Types (id, name, category, parameters)
    - [x] Workouts (id, name, planned_date, status)
  - [x] Initial migration with indexes
  - [x] Development Environment
    - [x] Set up environment configuration
    - [x] Add development database configuration
    - [x] Create environment switching scripts
  - [x] Sample Data
    - [x] Create dummy users
    - [x] Add sample exercise types
    - [x] Generate example training plans
    - [x] Add sample workouts
  - [x] Development Documentation
    - [x] Database setup guide
    - [x] Environment configuration
    - [x] Sample data documentation

- [x] Basic Backend
  - [x] SQLAlchemy models
  - [x] Essential endpoints:
    - [x] User creation/access
    - [x] Training plan CRUD
    - [x] Workout management
    - [x] Exercise type listing
  - [x] API Documentation
  - [x] Organized project structure:
    - [x] Core components (models, config)
    - [x] Route definitions
    - [x] Development scripts
    - [x] Migration setup

### Day 2: UI Implementation 🚧

#### 1. Technical Setup ✅
##### Framework & Tools
- [x] Next.js 15 (App Router)
  - [x] React Server Components
  - [x] Server Actions
  - [x] Built-in optimizations
- [x] TypeScript
- [x] ESLint & Prettier

##### UI Libraries
- [x] Tailwind CSS
- [x] Shadcn UI
- [x] Lucide Icons

##### Data Management
- [x] React Query
- [x] React Hook Form
- [x] date-fns
- [x] @fullcalendar/react

#### 2. Core Implementation ✅
##### Project Structure
- [x] Configure Next.js app
- [x] Set up component hierarchy
- [x] Create API client utilities
- [x] Implement base layout

##### Essential Components
- [x] Loading states
- [x] Error states
- [x] Empty states
- [x] Basic responsive layout

#### 3. Feature Implementation 🚧
##### User Management ✅
- [x] Access key entry screen
- [x] Basic profile display
- [x] Error handling

##### Training Plans ✅
- [x] Plan list view
- [x] Creation form
- [x] Details view
- [x] Edit/delete actions

##### Workouts (NEXT UP 👉)
- [x] Database Updates
  - [x] Add workout_exercises table
  - [x] Create many-to-many relationship between workouts and exercises
  - [x] Update workout creation endpoint to handle exercises
  - [x] Add endpoint to update workout exercises
  - [x] Update workout retrieval to include exercises
- [x] Calendar view
  - [x] FullCalendar integration
  - [x] Workout display
  - [x] Status color coding
  - [x] Click handling for status updates
- [x] Basic creation flow
  - [x] Date picker
  - [x] Exercise selector
  - [x] Form validation
  - [x] Error handling
- [x] Status management
  - [x] Status cycling (planned -> completed -> skipped)
  - [x] Visual status indicators
  - [x] Status update API integration
- [x] List view
  - [x] Workout cards
  - [x] Status controls
  - [x] Delete functionality
  - [x] Loading states

##### Exercise Browser
- [x] Type listing
  - [x] Exercise cards
  - [x] Category display
- [x] Basic search
  - [x] Real-time filtering
  - [x] Name and category search
- [x] Selection interface
  - [x] Exercise picker modal
  - [x] Selected exercise management
  - [x] Integration with workout form

### Technical Stack & Dependencies
- [x] Core Framework
  - [x] Next.js 15 (App Router)
    - [x] React Server Components for performance
    - [x] Server Actions for form handling
    - [x] Built-in Image and Font optimization

- [x] UI & Styling
  - [x] Tailwind CSS for styling
  - [x] Shadcn UI for component library
  - [x] Lucide Icons for iconography

- [x] Data Management & Forms
  - [x] React Query for server state
  - [x] React Hook Form for form handling
  - [x] date-fns for date manipulation

- [x] Calendar & Scheduling
  - [x] @fullcalendar/react for workout scheduling

- [x] Development Tools
  - [x] TypeScript for type safety
  - [x] ESLint & Prettier for code quality

- [x] Essential Frontend Setup
  - [x] Configure Next.js project structure
  - [x] Set up Shadcn UI and Tailwind
  - [x] Create API client utilities
  - [x] Basic responsive layout

- [x] User Management UI
  - [x] Access key entry screen
  - [x] Basic user profile display
  - [x] Error handling for invalid access

- [x] Training Plan Interface
  - [x] Training plan list view
  - [x] Plan creation form
  - [x] Plan details view
  - [x] Basic edit/delete functionality

- [x] Workout Management
  - [x] Calendar view for scheduling
  - [x] Basic workout creation
    - [x] Date selection
    - [x] Exercise selection
  - [x] Workout status updates
  - [x] List view of workouts

- [x] Exercise Type Browser
  - [x] Simple exercise type listing
  - [x] Basic search functionality

- [x] Core UI Components
  - [x] Loading states
  - [x] Error states
  - [x] Empty states
  - [x] Success/error notifications

## Features for Production
### Authentication & Security
- [ ] Database Changes
  - [ ] Update User model:
    - [ ] Add email (unique, required)
    - [ ] Add password (hashed, required)
    - [ ] Add email_verified (boolean)
    - [ ] Add verification_token
    - [ ] Remove access_key field
  - [ ] Create new migration
  - [ ] Update existing data (if any)

- [ ] Authentication Backend
  - [ ] Add Flask-Login integration
  - [ ] Add password hashing with werkzeug.security
  - [ ] Create login endpoint (/api/auth/login)
  - [ ] Create register endpoint (/api/auth/register)
  - [ ] Create logout endpoint (/api/auth/logout)
  - [ ] Add session management
  - [ ] Add @login_required decorators to protected routes

- [ ] Email Verification
  - [ ] Set up smtplib for email sending
  - [ ] Create verification token generation
  - [ ] Create email templates
  - [ ] Add verify endpoint (/api/auth/verify/<token>)
  - [ ] Add resend verification endpoint

- [ ] Security Enhancements
  - [ ] Add rate limiting for auth endpoints
  - [ ] Add password reset functionality
  - [ ] Update CORS settings
  - [ ] Add CSRF protection
  - [ ] Add secure session configuration

### Enhanced Frontend Features
- [ ] Advanced UI & Accessibility
  - [ ] Radix UI primitives integration
  - [ ] Advanced component animations
  - [ ] Full keyboard navigation
  - [ ] Screen reader optimization
  - [ ] High contrast mode

- [ ] Advanced Data Management
  - [ ] Zod schema validation
  - [ ] Advanced form validation
  - [ ] Optimistic updates
  - [ ] Offline support
  - [ ] Real-time sync

- [ ] Enhanced Exercise Management
  - [ ] Advanced exercise type browser
    - [ ] Categorized view
    - [ ] Filters and tags
    - [ ] Exercise details modal
    - [ ] Exercise history tracking
  - [ ] Parameter configuration UI
  - [ ] Exercise variation system

- [ ] Advanced Workout Features
  - [ ] Detailed workout builder
  - [ ] Exercise sequencing
  - [ ] Rest timer integration
  - [ ] Progress tracking
  - [ ] Performance analytics

- [ ] Data Visualization
  - [ ] Recharts integration
  - [ ] Progress graphs
  - [ ] Performance trends
  - [ ] Training volume analysis

- [ ] Testing Infrastructure
  - [ ] Jest setup
  - [ ] React Testing Library
  - [ ] Cypress E2E tests
  - [ ] Playwright cross-browser tests
  - [ ] Performance testing
  - [ ] Accessibility testing

- [ ] Mobile Optimizations
  - [ ] Touch gesture support
  - [ ] PWA setup
  - [ ] Offline functionality
  - [ ] Push notifications

- [ ] Development Experience
  - [ ] Husky git hooks
  - [ ] Advanced ESLint rules
  - [ ] Storybook component library
  - [ ] API documentation
  - [ ] Component documentation

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
  - [x] Basic endpoint documentation
  - [x] API structure documentation
  - [ ] OpenAPI/Swagger integration
  - [ ] Authentication documentation

### Frontend Features
- [ ] Advanced UI components
  - [ ] Training block designer
  - [ ] Progress graphs
  - [ ] Exercise history
- [ ] State management
- [ ] Real-time updates

### Development Tools
- [x] Basic testing infrastructure
  - [x] Database verification script
  - [ ] API endpoint tests
  - [ ] Model tests
- [ ] CI/CD pipeline
- [x] Development environment setup
  - [x] Database configuration
  - [x] Environment variables
  - [x] Project structure
- [ ] Production deployment
  - [ ] Configure HTTPS in Vercel for production
  - [ ] Set up proper SSL certificates
  - [ ] Configure domain settings
  - [ ] Test secure API endpoints

### Monitoring & Optimization
- [ ] Performance monitoring
- [ ] Query optimization
- [ ] Usage analytics

##### Next Steps 👉
- [ ] Enhanced Exercise Features
  - [ ] Exercise details modal
  - [ ] Exercise history tracking
  - [ ] Parameter configuration UI
  - [ ] Exercise variation system

---
Note: MVP focuses on core training plan and workout management. Additional features will be added based on user feedback.