package com.platform.service;

import com.platform.model.Metric;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class MonitoringService {

    private final JdbcTemplate jdbc;

    public MonitoringService(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    private final RowMapper<Metric> metricMapper = (rs, rowNum) -> {
        Metric m = new Metric();
        m.setId(rs.getLong("id"));
        m.setContainerName(rs.getString("container_name"));
        m.setCpuPercent(rs.getDouble("cpu_percent"));
        m.setMemoryUsageMb(rs.getDouble("memory_usage_mb"));
        m.setMemoryPercent(rs.getDouble("memory_percent"));
        m.setNetworkRx(rs.getLong("network_rx"));
        m.setNetworkTx(rs.getLong("network_tx"));
        return m;
    };

    public List<Metric> getMetrics(String containerName, int limit) {
        return jdbc.query(
            "SELECT * FROM metrics WHERE container_name = ? ORDER BY collected_at DESC LIMIT ?",
            metricMapper, containerName, limit
        );
    }

    public Map<String, Object> getMetricAvg(String containerName, int minutes) {
        Map<String, Object> result = jdbc.queryForMap(
            "SELECT " +
            "AVG(cpu_percent) as avg_cpu, " +
            "AVG(memory_percent) as avg_memory, " +
            "MAX(cpu_percent) as max_cpu, " +
            "MAX(memory_percent) as max_memory, " +
            "COUNT(*) as sample_count " +
            "FROM metrics WHERE container_name = ? " +
            "AND collected_at >= datetime('now', '-' || ? || ' minutes')",
            containerName, minutes
        );
        return result;
    }

    public List<Map<String, Object>> getActiveAlerts() {
        return jdbc.queryForList(
            "SELECT * FROM alerts WHERE resolved = 0 ORDER BY created_at DESC"
        );
    }

    public Map<String, Object> getAlertSummary() {
        Map<String, Object> summary = new HashMap<>();
        List<Map<String, Object>> active = getActiveAlerts();
        summary.put("total_active", active.size());
        summary.put("critical", active.stream()
            .filter(a -> "critical".equals(a.get("severity"))).count());
        summary.put("warning", active.stream()
            .filter(a -> "warning".equals(a.get("severity"))).count());
        summary.put("alerts", active);
        return summary;
    }

    public Map<String, Object> getDashboardData() {
        Map<String, Object> data = new HashMap<>();

        // 컨테이너 수
        data.put("containers", jdbc.queryForList(
            "SELECT * FROM containers ORDER BY created_at DESC"
        ));

        // 최근 메트릭
        data.put("recent_metrics", jdbc.queryForList(
            "SELECT container_name, " +
            "AVG(cpu_percent) as avg_cpu, " +
            "AVG(memory_percent) as avg_memory " +
            "FROM metrics " +
            "WHERE collected_at >= datetime('now', '-5 minutes') " +
            "GROUP BY container_name"
        ));

        // 알림
        data.put("alerts", getAlertSummary());

        // 최근 이벤트
        data.put("recent_events", jdbc.queryForList(
            "SELECT * FROM events ORDER BY created_at DESC LIMIT 10"
        ));

        return data;
    }
}
