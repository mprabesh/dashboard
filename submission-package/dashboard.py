#!/usr/bin/env python3
"""
Python Dashboard Application
Tech Stack: Python 3.x, Tkinter, Matplotlib, Pandas
Data Source: metrics.json
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import json
import os
import signal
import sys
from datetime import datetime, timedelta
import numpy as np

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Dashboard - Multi-CSV Data Visualization")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f0f0")
        
        # Data storage
        self.data = None
        self.metrics_file = "metrics.json"
        self.current_file = None
        self.available_csv_files = []
        
        # Discover available CSV files
        self.discover_csv_files()
        
        # Create GUI components
        self.create_widgets()
        
        # Load default data - try to load the first available CSV, then fallback to JSON
        if self.available_csv_files and self.available_csv_files[0] != "No CSV files found":
            self.csv_file_var.set(self.available_csv_files[0])
            self.load_selected_csv()
        else:
            self.load_data()
        
    def create_widgets(self):
        """Create and layout GUI components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Multi-CSV Data Dashboard", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Control panel (left side)
        control_frame = ttk.LabelFrame(main_frame, text="Data & Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # CSV File selection
        ttk.Label(control_frame, text="Select CSV File:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.csv_file_var = tk.StringVar()
        self.csv_combo = ttk.Combobox(control_frame, textvariable=self.csv_file_var, 
                                     values=self.available_csv_files, state="readonly")
        self.csv_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        self.csv_combo.bind("<<ComboboxSelected>>", self.load_selected_csv)
        
        # Load data buttons
        load_btn = ttk.Button(control_frame, text="Load JSON Data", command=self.load_data)
        load_btn.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 5))
        
        # Load custom file button
        load_file_btn = ttk.Button(control_frame, text="Load Custom File", 
                                  command=self.load_custom_file)
        load_file_btn.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Chart type selection
        ttk.Label(control_frame, text="Chart Type:").grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        self.chart_type = tk.StringVar(value="line")
        chart_combo = ttk.Combobox(control_frame, textvariable=self.chart_type,
                                  values=["line", "bar", "scatter", "pie", "histogram", "box"], state="readonly")
        chart_combo.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        chart_combo.bind("<<ComboboxSelected>>", self.update_chart)
        
        # Metric selection
        ttk.Label(control_frame, text="Primary Metric:").grid(row=6, column=0, sticky=tk.W, pady=(10, 5))
        self.metric_var = tk.StringVar()
        self.metric_combo = ttk.Combobox(control_frame, textvariable=self.metric_var, state="readonly")
        self.metric_combo.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        self.metric_combo.bind("<<ComboboxSelected>>", self.update_chart)
        
        # Secondary metric (for scatter plots)
        ttk.Label(control_frame, text="Secondary Metric:").grid(row=8, column=0, sticky=tk.W, pady=(10, 5))
        self.metric2_var = tk.StringVar()
        self.metric2_combo = ttk.Combobox(control_frame, textvariable=self.metric2_var, state="readonly")
        self.metric2_combo.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        self.metric2_combo.bind("<<ComboboxSelected>>", self.update_chart)
        
        # Group by selection (for categorical data)
        ttk.Label(control_frame, text="Group By:").grid(row=10, column=0, sticky=tk.W, pady=(10, 5))
        self.groupby_var = tk.StringVar()
        self.groupby_combo = ttk.Combobox(control_frame, textvariable=self.groupby_var, state="readonly")
        self.groupby_combo.grid(row=11, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        self.groupby_combo.bind("<<ComboboxSelected>>", self.update_chart)
        
        # Refresh button
        refresh_btn = ttk.Button(control_frame, text="Refresh Chart", command=self.update_chart)
        refresh_btn.grid(row=12, column=0, sticky=(tk.W, tk.E), pady=(10, 5))
        
        # Export button
        export_btn = ttk.Button(control_frame, text="Export Chart", command=self.export_chart)
        export_btn.grid(row=13, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Data preview
        ttk.Label(control_frame, text="Data Preview:").grid(row=14, column=0, sticky=tk.W, pady=(10, 5))
        self.preview_text = tk.Text(control_frame, height=8, width=35, wrap=tk.WORD, font=("Consolas", 9))
        preview_scroll = ttk.Scrollbar(control_frame, orient="vertical", command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scroll.set)
        self.preview_text.grid(row=15, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Info text
        self.info_text = tk.Text(control_frame, height=4, width=35, wrap=tk.WORD, font=("Arial", 9))
        self.info_text.grid(row=16, column=0, sticky=(tk.W, tk.E), pady=(0, 0))
        
        # Chart area (right side)
        chart_frame = ttk.LabelFrame(main_frame, text="Visualization", padding="10")
        chart_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.fig.patch.set_facecolor('white')
        
        # Create canvas for matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configure column weights
        control_frame.columnconfigure(0, weight=1)
        
    def discover_csv_files(self):
        """Discover available CSV files in the current directory"""
        import glob
        csv_files = glob.glob("*.csv")
        self.available_csv_files = [f for f in csv_files if f != 'sample_data.csv']  # Exclude the old sample
        if not self.available_csv_files:
            self.available_csv_files = ["No CSV files found"]
    
    def load_selected_csv(self, event=None):
        """Load the selected CSV file"""
        selected_file = self.csv_file_var.get()
        if selected_file and selected_file != "No CSV files found":
            try:
                self.data = pd.read_csv(selected_file)
                self.current_file = selected_file
                self.update_column_options()
                self.update_preview()
                self.update_info(f"Loaded CSV: {selected_file}")
                self.update_chart()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {str(e)}")
                
    def update_column_options(self):
        """Update the dropdown options based on loaded data"""
        if self.data is not None:
            # Get numeric and categorical columns
            numeric_columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
            all_columns = self.data.columns.tolist()
            categorical_columns = self.data.select_dtypes(include=['object', 'category']).columns.tolist()
            
            # Update metric combo boxes
            if numeric_columns:
                self.metric_combo['values'] = numeric_columns
                self.metric2_combo['values'] = numeric_columns
                self.metric_var.set(numeric_columns[0])
                if len(numeric_columns) > 1:
                    self.metric2_var.set(numeric_columns[1])
            
            # Update group by combo box with Week as priority default
            groupby_options = ['None'] + categorical_columns
            if 'date' in all_columns or 'Date' in all_columns:
                date_cols = [col for col in all_columns if col.lower() in ['date']]
                groupby_options.extend(date_cols)
            
            self.groupby_combo['values'] = groupby_options
            
            # Set default groupby - prioritize Week, then other options
            if 'Week' in all_columns:
                self.groupby_var.set('Week')
            elif 'week' in all_columns:
                self.groupby_var.set('week')
            elif categorical_columns:
                self.groupby_var.set(categorical_columns[0])
            else:
                self.groupby_var.set('None')
    
    def update_preview(self):
        """Update the data preview text area"""
        if self.data is not None:
            self.preview_text.delete(1.0, tk.END)
            
            # Show basic info
            preview_info = f"File: {self.current_file}\n"
            preview_info += f"Shape: {self.data.shape}\n"
            preview_info += f"Columns: {', '.join(self.data.columns.tolist())}\n\n"
            
            # Show first few rows
            preview_info += "First 5 rows:\n"
            preview_info += self.data.head().to_string()
            
            self.preview_text.insert(tk.END, preview_info)
        
    def load_data(self):
        """Load data from metrics.json file"""
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r') as file:
                    data = json.load(file)
                    self.process_data(data)
                    self.update_info(f"Loaded data from {self.metrics_file}")
            else:
                self.create_sample_data()
                messagebox.showinfo("Info", f"Created sample {self.metrics_file} file")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            
    def load_custom_file(self):
        """Load data from a custom JSON or CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.data = pd.read_csv(file_path)
                    self.current_file = os.path.basename(file_path)
                    self.update_column_options()
                    self.update_preview()
                elif file_path.endswith('.json'):
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        self.process_data(data)
                    
                self.update_info(f"Loaded data from {os.path.basename(file_path)}")
                self.update_chart()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def process_data(self, data):
        """Process loaded data and update UI"""
        if isinstance(data, dict) and 'metrics' in data:
            self.data = pd.DataFrame(data['metrics'])
            self.current_file = "metrics.json"
        elif isinstance(data, list):
            self.data = pd.DataFrame(data)
            self.current_file = "JSON data"
        else:
            self.data = pd.DataFrame([data])
            self.current_file = "JSON data"
        
        # Update UI components
        self.update_column_options()
        self.update_preview()
        self.update_chart()
        
    def create_sample_data(self):
        """Create sample metrics.json file"""
        # Generate sample data
        dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
        
        sample_data = {
            "metadata": {
                "source": "Sample Dashboard Data",
                "generated": datetime.now().isoformat(),
                "description": "Sample metrics for dashboard demonstration"
            },
            "metrics": [
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "revenue": round(np.random.normal(10000, 2000), 2),
                    "users": int(np.random.normal(500, 100)),
                    "conversion_rate": round(np.random.normal(0.15, 0.05), 3),
                    "page_views": int(np.random.normal(5000, 1000)),
                    "bounce_rate": round(np.random.normal(0.4, 0.1), 3)
                }
                for date in dates
            ]
        }
        
        with open(self.metrics_file, 'w') as file:
            json.dump(sample_data, file, indent=2)
            
        self.process_data(sample_data)
        
    def update_chart(self, event=None):
        """Update the chart based on current selections"""
        if self.data is None or self.data.empty:
            return
            
        self.ax.clear()
        
        chart_type = self.chart_type.get()
        metric = self.metric_var.get()
        metric2 = self.metric2_var.get()
        groupby = self.groupby_var.get()
        
        if not metric:
            return
            
        try:
            if chart_type == "line":
                if groupby and groupby != 'None':
                    # Special handling for Week grouping
                    if groupby.lower() == 'week':
                        # Sort by week number for proper chronological order
                        if 'Week' in self.data.columns:
                            # Extract week numbers for proper sorting
                            self.data['week_num'] = self.data['Week'].str.extract(r'(\d+)').astype(int)
                            sorted_data = self.data.sort_values('week_num')
                            self.ax.plot(sorted_data['Week'], sorted_data[metric], marker='o', linewidth=2, label=metric)
                            self.ax.set_xlabel("Week")
                        else:
                            # Fallback for other week column formats
                            self.ax.plot(self.data[groupby], self.data[metric], marker='o', linewidth=2)
                            self.ax.set_xlabel(groupby)
                    else:
                        # Group by other categorical variables
                        for name, group in self.data.groupby(groupby):
                            if 'date' in self.data.columns.str.lower():
                                date_col = [col for col in self.data.columns if 'date' in col.lower()][0]
                                group[date_col] = pd.to_datetime(group[date_col], errors='coerce')
                                self.ax.plot(group[date_col], group[metric], marker='o', label=str(name), linewidth=2)
                            else:
                                self.ax.plot(group.index, group[metric], marker='o', label=str(name), linewidth=2)
                        self.ax.legend()
                else:
                    if 'date' in self.data.columns.str.lower():
                        date_col = [col for col in self.data.columns if 'date' in col.lower()][0]
                        date_series = pd.to_datetime(self.data[date_col], errors='coerce')
                        self.ax.plot(date_series, self.data[metric], marker='o', linewidth=2)
                        self.ax.set_xlabel("Date")
                    elif 'Week' in self.data.columns:
                        # Default to Week if available
                        self.ax.plot(self.data['Week'], self.data[metric], marker='o', linewidth=2)
                        self.ax.set_xlabel("Week")
                    else:
                        self.ax.plot(self.data.index, self.data[metric], marker='o', linewidth=2)
                        self.ax.set_xlabel("Index")
                
                self.ax.set_ylabel(metric.replace('_', ' ').title())
                self.ax.set_title(f"{metric.replace('_', ' ').title()} Over Time")
                
            elif chart_type == "bar":
                if groupby and groupby != 'None':
                    if groupby.lower() == 'week':
                        # Special handling for Week - show all weeks in order
                        if 'Week' in self.data.columns:
                            self.data['week_num'] = self.data['Week'].str.extract(r'(\d+)').astype(int)
                            sorted_data = self.data.sort_values('week_num')
                            self.ax.bar(range(len(sorted_data)), sorted_data[metric])
                            self.ax.set_xticks(range(len(sorted_data)))
                            self.ax.set_xticklabels(sorted_data['Week'], rotation=45, ha='right')
                            self.ax.set_xlabel("Week")
                        else:
                            grouped_data = self.data.groupby(groupby)[metric].sum().sort_index()
                            self.ax.bar(range(len(grouped_data)), grouped_data.values)
                            self.ax.set_xticks(range(len(grouped_data)))
                            self.ax.set_xticklabels(grouped_data.index, rotation=45, ha='right')
                            self.ax.set_xlabel(groupby.replace('_', ' ').title())
                    else:
                        grouped_data = self.data.groupby(groupby)[metric].sum().sort_values(ascending=False)
                        self.ax.bar(range(len(grouped_data)), grouped_data.values)
                        self.ax.set_xticks(range(len(grouped_data)))
                        self.ax.set_xticklabels(grouped_data.index, rotation=45, ha='right')
                        self.ax.set_xlabel(groupby.replace('_', ' ').title())
                else:
                    if len(self.data) > 20:
                        data_subset = self.data.tail(20)
                        self.ax.bar(range(len(data_subset)), data_subset[metric])
                        self.ax.set_xlabel("Recent Records")
                    else:
                        self.ax.bar(range(len(self.data)), self.data[metric])
                        if 'Week' in self.data.columns:
                            self.ax.set_xticks(range(len(self.data)))
                            self.ax.set_xticklabels(self.data['Week'], rotation=45, ha='right')
                            self.ax.set_xlabel("Week")
                        else:
                            self.ax.set_xlabel("Records")
                
                self.ax.set_ylabel(metric.replace('_', ' ').title())
                self.ax.set_title(f"{metric.replace('_', ' ').title()} by {groupby if groupby and groupby != 'None' else 'Period'}")
                
            elif chart_type == "scatter":
                if metric2:
                    if groupby and groupby != 'None':
                        for name, group in self.data.groupby(groupby):
                            self.ax.scatter(group[metric], group[metric2], alpha=0.7, label=str(name))
                        self.ax.legend()
                    else:
                        self.ax.scatter(self.data[metric], self.data[metric2], alpha=0.7)
                    
                    self.ax.set_xlabel(metric.replace('_', ' ').title())
                    self.ax.set_ylabel(metric2.replace('_', ' ').title())
                    self.ax.set_title(f"{metric.replace('_', ' ').title()} vs {metric2.replace('_', ' ').title()}")
                
            elif chart_type == "pie":
                if groupby and groupby != 'None':
                    grouped_data = self.data.groupby(groupby)[metric].sum()
                    self.ax.pie(grouped_data.values, labels=grouped_data.index, autopct='%1.1f%%')
                    self.ax.set_title(f"{metric.replace('_', ' ').title()} by {groupby.replace('_', ' ').title()}")
                else:
                    # Create bins for numeric data
                    if self.data[metric].dtype in ['object', 'category']:
                        value_counts = self.data[metric].value_counts()
                        self.ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
                    else:
                        bins = pd.cut(self.data[metric], bins=5)
                        bin_counts = bins.value_counts()
                        self.ax.pie(bin_counts.values, labels=[str(x) for x in bin_counts.index], autopct='%1.1f%%')
                    self.ax.set_title(f"{metric.replace('_', ' ').title()} Distribution")
                    
            elif chart_type == "histogram":
                self.ax.hist(self.data[metric].dropna(), bins=20, alpha=0.7, edgecolor='black')
                self.ax.set_xlabel(metric.replace('_', ' ').title())
                self.ax.set_ylabel("Frequency")
                self.ax.set_title(f"{metric.replace('_', ' ').title()} Histogram")
                
            elif chart_type == "box":
                if groupby and groupby != 'None':
                    box_data = [group[metric].dropna() for name, group in self.data.groupby(groupby)]
                    box_labels = [str(name) for name, group in self.data.groupby(groupby)]
                    self.ax.boxplot(box_data, labels=box_labels)
                    self.ax.set_xlabel(groupby.replace('_', ' ').title())
                else:
                    self.ax.boxplot(self.data[metric].dropna())
                    self.ax.set_xticklabels([metric.replace('_', ' ').title()])
                
                self.ax.set_ylabel(metric.replace('_', ' ').title())
                self.ax.set_title(f"{metric.replace('_', ' ').title()} Box Plot")
                
            self.ax.grid(True, alpha=0.3)
            plt.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to create chart: {str(e)}")
            print(f"Chart error details: {e}")  # For debugging
            
    def update_info(self, message):
        """Update the info text area"""
        info_text = f"Status: {message}\n\n"
        
        if self.data is not None:
            info_text += f"Data Shape: {self.data.shape}\n"
            info_text += f"Columns: {', '.join(self.data.columns.tolist())}\n\n"
            
            # Basic statistics for numeric columns
            numeric_data = self.data.select_dtypes(include=[np.number])
            if not numeric_data.empty:
                info_text += "Summary Statistics:\n"
                for col in numeric_data.columns[:3]:  # Show first 3 numeric columns
                    mean_val = numeric_data[col].mean()
                    info_text += f"{col}: μ={mean_val:.2f}\n"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info_text)
        
    def export_chart(self):
        """Export the current chart as an image"""
        if self.data is None:
            messagebox.showwarning("Warning", "No data to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Chart",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")]
        )
        
        if file_path:
            try:
                self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Success", f"Chart exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export chart: {str(e)}")

def main():
    """Main function to run the dashboard"""
    
    # Handle Ctrl+C and other signals gracefully
    def signal_handler(signum, frame):
        """Handle system signals to exit cleanly"""
        print("\n🛑 Dashboard interrupted. Cleaning up...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    root = tk.Tk()
    app = Dashboard(root)
    
    # Handle window closing properly
    def on_closing():
        """Handle window close event"""
        try:
            root.quit()  # Stop the mainloop
            root.destroy()  # Destroy the window
        except:
            pass
        finally:
            import sys
            sys.exit(0)  # Force exit the Python process
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (1400 // 2)
    y = (root.winfo_screenheight() // 2) - (900 // 2)
    root.geometry(f"1400x900+{x}+{y}")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        on_closing()
    except:
        on_closing()

if __name__ == "__main__":
    main()
