-- 🔥 FANER STUDIO - SUPABASE DATABASE SETUP
-- Copy ALL of this and paste into Supabase SQL Editor

-- ============================================================
-- CREATE TABLES
-- ============================================================

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Projects table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    project_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    progress FLOAT DEFAULT 0.0,
    voice_id VARCHAR(100),
    input_file VARCHAR(500),
    output_files TEXT,
    settings TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Custom Voices table
CREATE TABLE custom_voices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    voice_id VARCHAR(100) UNIQUE NOT NULL,
    voice_name VARCHAR(200) NOT NULL,
    speaker_name VARCHAR(200),
    language VARCHAR(10) DEFAULT 'ht',
    gender VARCHAR(20) DEFAULT 'unknown',
    age_range VARCHAR(20) DEFAULT 'adult',
    region VARCHAR(100) DEFAULT 'Haiti',
    audio_file VARCHAR(500) NOT NULL,
    audio_format VARCHAR(10) NOT NULL,
    duration_seconds FLOAT DEFAULT 0.0,
    file_size_mb FLOAT DEFAULT 0.0,
    text_content TEXT,
    notes TEXT,
    times_used INTEGER DEFAULT 0,
    rating FLOAT DEFAULT 0.0,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- API Keys table
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    key_name VARCHAR(100) NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used TIMESTAMP,
    expires_at TIMESTAMP
);

-- Activity Logs table
CREATE TABLE activity_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,
    endpoint VARCHAR(200),
    status_code INTEGER,
    ip_address VARCHAR(45),
    user_agent TEXT,
    request_data TEXT,
    response_data TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- CREATE INDEXES (for better performance)
-- ============================================================

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_custom_voices_user_id ON custom_voices(user_id);
CREATE INDEX idx_custom_voices_voice_id ON custom_voices(voice_id);
CREATE INDEX idx_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX idx_activity_logs_created_at ON activity_logs(created_at);

-- ============================================================
-- ENABLE ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE custom_voices ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_logs ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- RLS POLICIES - Users
-- ============================================================

CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- ============================================================
-- RLS POLICIES - Projects
-- ============================================================

CREATE POLICY "Users can view own projects" ON projects
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own projects" ON projects
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own projects" ON projects
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own projects" ON projects
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- ============================================================
-- RLS POLICIES - Custom Voices
-- ============================================================

CREATE POLICY "Users can view own voices" ON custom_voices
    FOR SELECT USING (auth.uid()::text = user_id::text OR is_public = TRUE);

CREATE POLICY "Users can insert own voices" ON custom_voices
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own voices" ON custom_voices
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own voices" ON custom_voices
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- ============================================================
-- DONE!
-- ============================================================
-- You should see: "Success. No rows returned"
-- If you see errors, read them carefully and fix any issues

