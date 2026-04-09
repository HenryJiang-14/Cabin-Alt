# 标记是否已经显示过警告
_barometer_warning_shown = False

def get_pressure():
    global _barometer_warning_shown
    try:
        from plyer import barometer
        pressure = barometer.pressure
        
        # 检查返回值
        if pressure is None:
            if not _barometer_warning_shown:
                print("Barometer returned None")
                _barometer_warning_shown = True
            return 1013.25
        
        # 检查是否是有效数值
        if isinstance(pressure, (int, float)) and pressure > 0:
            return float(pressure)
        else:
            if not _barometer_warning_shown:
                print(f"Barometer returned invalid value: {pressure}")
                _barometer_warning_shown = True
            return 1013.25
            
    except Exception as e:
        # Windows 不支持气压计,返回默认值用于测试
        if not _barometer_warning_shown:
            print(f"Barometer not available (using default value): {e}")
            _barometer_warning_shown = True
        return 1013.25