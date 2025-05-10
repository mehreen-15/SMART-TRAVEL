from django.db import models
import datetime

class DatabaseConnectionLog(models.Model):
    """
    Model to track database connection information and performance metrics.
    This helps track SQLite usage patterns and performance over time.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    connection_id = models.CharField(max_length=100)
    user_agent = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    query_count = models.PositiveIntegerField(default=0)
    query_time_ms = models.PositiveIntegerField(default=0)
    tables_accessed = models.TextField(null=True, blank=True)
    
    # SQLite specific metrics
    journal_mode = models.CharField(max_length=50, null=True, blank=True)
    page_size = models.PositiveIntegerField(null=True, blank=True)
    cache_size = models.IntegerField(null=True, blank=True)
    sqlite_version = models.CharField(max_length=20, null=True, blank=True)
    
    class Meta:
        verbose_name = "Database Connection Log"
        verbose_name_plural = "Database Connection Logs"
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"Connection {self.connection_id} at {self.timestamp}"
    
    @property
    def connection_duration(self):
        """Calculate the duration of the connection in seconds"""
        if hasattr(self, 'connection_end'):
            return (self.connection_end - self.timestamp).total_seconds()
        return (datetime.datetime.now() - self.timestamp.replace(tzinfo=None)).total_seconds()
    
    @property
    def avg_query_time(self):
        """Calculate the average query time in milliseconds"""
        if self.query_count > 0:
            return self.query_time_ms / self.query_count
        return 0

class DatabaseStatus(models.Model):
    """
    Model to store current database status and configuration.
    Updated periodically to track database health and settings.
    """
    last_update = models.DateTimeField(auto_now=True)
    engine = models.CharField(max_length=50, default="SQLite")
    version = models.CharField(max_length=20)
    size_bytes = models.BigIntegerField(default=0)
    table_count = models.PositiveIntegerField(default=0)
    index_count = models.PositiveIntegerField(default=0)
    journal_mode = models.CharField(max_length=20, default="delete")
    synchronous_setting = models.IntegerField(default=2)
    cache_size = models.IntegerField(default=2000)
    page_size = models.IntegerField(default=4096)
    last_vacuum = models.DateTimeField(null=True, blank=True)
    integrity_check = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Database Status"
        verbose_name_plural = "Database Status"
        
    def __str__(self):
        return f"{self.engine} {self.version} - Last Updated: {self.last_update}"
    
    @property
    def size_mb(self):
        """Return the database size in megabytes"""
        return round(self.size_bytes / (1024 * 1024), 2)
    
    @property
    def health_status(self):
        """Determine the health status of the database"""
        if self.integrity_check and self.integrity_check != "ok":
            return "Critical"
        
        # Check if database was vacuumed recently (within 30 days)
        if not self.last_vacuum or (datetime.datetime.now() - self.last_vacuum.replace(tzinfo=None)).days > 30:
            return "Warning"
            
        return "Good" 