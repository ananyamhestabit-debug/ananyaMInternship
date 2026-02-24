# Week 4 – Day 1  
## Backend System Architecture Documentation
### 1. Introduction

In this task, I built the foundational structure of a backend system using Node.js, Express, and MongoDB.

The main objective of this setup was not to build full APIs, but to design a clean and scalable backend structure that can be safely extended in the future.
The focus areas were:
- Environment-based configuration
- Structured folder organization
- Controlled application startup
- Proper database initialization
- Logging system
- Graceful shutdown handling

This architecture ensures that the backend is production-ready from the beginning.

### 2. Folder Structure and Design Thinking

Instead of writing everything in one file, I separated the system into structured folders inside `src/`.

This separation helps in maintaining clarity and scalability.

src/
  config/
  loaders/
  models/
  routes/
  controllers/
  services/
  repositories/
  middlewares/
  utils/
  jobs/
  logs/

Below is the purpose of each folder:

**config/**  
Handles environment configuration.  
This ensures that sensitive values like PORT and DATABASE_URL are not hardcoded in the application.

**loaders/**  
Responsible for system startup logic.  
This includes:
- Database connection setup
- Express app initialization  
This helps in controlling the startup lifecycle.

**models/**  
Will store database schemas in future development.

**routes/**  
Defines API endpoint mappings.  
This layer decides which controller handles which request.

**controllers/**  
Handles incoming HTTP requests and sends responses back to the client.

**services/**  
Contains business logic.  
This ensures controllers remain clean and focused only on request handling.

**repositories/**  
Responsible for direct interaction with the database.  
This keeps database logic separated from business logic.

**middlewares/**  
Contains reusable request-processing functions such as JSON parsing, authentication, etc.

**utils/**  
Stores helper utilities like the logger configuration.

**jobs/**  
Reserved for background tasks (for future scalability).

**logs/**  
Reserved for storing production log files.

This structured approach follows the principle of separation of concerns.

### 3. Application Startup Lifecycle

The application does not start randomly.  
It follows a defined startup sequence:

1. Configuration is loaded based on NODE_ENV.
2. Logger is initialized.
3. Express application is created.
4. Middlewares are applied.
5. Routes are mounted.
6. Database connection is established.
7. Server starts listening on the configured port.

If the database connection fails, the application exits immediately.

This "fail fast" strategy ensures that the system does not run in a broken state.

### 4. Environment Management Strategy

To maintain separation between development and production, I created three environment files:
- .env.local
- .env.dev
- .env.prod

The correct file is selected dynamically using:

process.env.NODE_ENV

If no environment is specified, the system defaults to "local".
This prevents accidental usage of production credentials during development.

### 5. Logging Strategy

Instead of using console.log, I implemented structured logging using Pino.
The logger records:
- Middleware loading
- Route mounting
- Database connection status
- Server startup
- Shutdown events

This approach improves debugging and production monitoring.

### 6. Database Initialization Strategy

The MongoDB connection is established during startup using Mongoose.
If the connection fails:
- An error is logged
- The application exits immediately

This ensures the server does not accept requests without a working database connection.

### 7. Graceful Shutdown Handling

The application listens for process termination signals (SIGINT).
During shutdown:
1. Database connection is closed.
2. Server stops accepting new requests.
3. The process exits safely.

This prevents incomplete operations or data corruption.

### 8. Design Principles Applied

While building this system, I applied the following principles:
- Separation of Concerns  
- Environment Isolation  
- Fail Fast Strategy  
- Modular Structure  
- Production-Oriented Logging  

### 9. Conclusion

This backend setup serves as a clean and scalable foundation.

Even though Day 1 does not include business features, the system is structured in a way that future development can be done without restructuring the core architecture.

The focus was on designing the system correctly from the beginning rather than building features quickly.