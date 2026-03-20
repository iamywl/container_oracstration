package com.platform.service;

import com.platform.model.Pipeline;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class PipelineService {

    private final JdbcTemplate jdbc;

    public PipelineService(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    private final RowMapper<Pipeline> pipelineMapper = (rs, rowNum) -> {
        Pipeline p = new Pipeline();
        p.setId(rs.getLong("id"));
        p.setPipelineId(rs.getString("pipeline_id"));
        p.setAppName(rs.getString("app_name"));
        p.setVersion(rs.getString("version"));
        p.setStage(rs.getString("stage"));
        p.setStatus(rs.getString("status"));
        p.setLogOutput(rs.getString("log_output"));
        p.setDurationS(rs.getObject("duration_s") != null ? rs.getInt("duration_s") : null);
        return p;
    };

    public List<Pipeline> getHistory(String appName, int limit) {
        if (appName != null) {
            return jdbc.query(
                "SELECT * FROM pipeline_runs WHERE app_name = ? ORDER BY started_at DESC LIMIT ?",
                pipelineMapper, appName, limit
            );
        }
        return jdbc.query(
            "SELECT * FROM pipeline_runs ORDER BY started_at DESC LIMIT ?",
            pipelineMapper, limit
        );
    }

    public List<Map<String, Object>> getDeployments(String service, String environment) {
        StringBuilder sql = new StringBuilder("SELECT * FROM deployments WHERE 1=1");
        if (service != null) {
            sql.append(" AND service = '").append(service).append("'");
        }
        if (environment != null) {
            sql.append(" AND environment = '").append(environment).append("'");
        }
        sql.append(" ORDER BY deployed_at DESC LIMIT 20");

        return jdbc.queryForList(sql.toString());
    }

    public Map<String, Object> getLatestDeployment(String service) {
        List<Map<String, Object>> results = jdbc.queryForList(
            "SELECT * FROM deployments WHERE service = ? AND rolled_back = 0 ORDER BY deployed_at DESC LIMIT 1",
            service
        );
        return results.isEmpty() ? null : results.get(0);
    }
}
