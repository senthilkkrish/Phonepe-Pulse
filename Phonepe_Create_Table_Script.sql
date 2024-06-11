# -----------------------------------------------------------#
# Aggregated State Transactions Table
# -----------------------------------------------------------#
CREATE TABLE phonepe.aggr_st_trans (
    State VARCHAR(255),
    Year VARCHAR(255),
    Quater INT,
    Transacion_type VARCHAR(255),
    Transacion_count BIGINT,
    Transacion_amount BIGINT
);
# -----------------------------------------------------------#
# Aggregated State Users Table
# -----------------------------------------------------------#
CREATE TABLE phonepe.aggr_st_users (
    State VARCHAR(255),
    Year VARCHAR(255),
    Quater INT,
    Brand_name VARCHAR(255),
    No_of_reg_users BIGINT,
    Percentage_share FLOAT
);
# -----------------------------------------------------------#
# Aggregated State Map Transactions Table
# -----------------------------------------------------------#
CREATE TABLE phonepe.map_st_trans (
    State VARCHAR(255),
    Year VARCHAR(255),
    Quater INT,
    District_name VARCHAR(255),
    Tot_No_of_Trans BIGINT,
    Tot_Trans_val FLOAT
);
# -----------------------------------------------------------#
# Aggregated State Map Insurance Table
# -----------------------------------------------------------#
CREATE TABLE phonepe.map_st_insur (
    State VARCHAR(255),
    Year VARCHAR(255),
    Quater INT,
    District_name VARCHAR(255),
    Tot_No_of_Insur BIGINT,
    Tot_Insur_value FLOAT
);
# -----------------------------------------------------------#
# Top 10 Users District Table
# -----------------------------------------------------------#
CREATE TABLE phonepe.top_st_users (
    State VARCHAR(255),
    Year VARCHAR(255),
    Quater INT,
    District_name VARCHAR(255),
    Registered_users BIGINT
);
# -----------------------------------------------------------#
# Top 10 Users Area code Table
# -----------------------------------------------------------#
CREATE TABLE phonepe.top_st_users_area (
    State VARCHAR(255),
    Year VARCHAR(255),
    Quater INT,
    Pin_code VARCHAR(255),
    Area_Reg_users BIGINT
);