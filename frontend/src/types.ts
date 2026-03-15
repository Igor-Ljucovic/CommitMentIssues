export type FileScanResult = {
  file_name: string;
  github_links: string[];
};

export type UploadResponse = {
  total_files: number;
  accepted_files: number;
  rejected_files: number;
  rejected_file_names: string[];
  scanned_files: FileScanResult[];
  unique_github_links: string[];
};

export type MetricParameterType = "int-range" | "date-range";

export type MetricParameterConfig = {
  key: string;
  label: string;
  type: MetricParameterType;
};

export type AnalysisItem = {
  name: string;
  parameters?: MetricParameterConfig[];
  tooltipText?: string;
  subItems?: AnalysisItem[];
};

export type AnalysisCategory = {
  title: string;
  items: AnalysisItem[];
};

export type AnalysisSelectionState = Record<string, Record<string, boolean>>;
export type CategoryWeightsState = Record<string, number>;
export type ItemWeightsState = Record<string, Record<string, number>>;

export type MetricParameterValue = {
  min?: string;
  max?: string;
  before?: string;
  after?: string;
};

export type MetricParametersState = Record<
  string,
  Record<string, Record<string, MetricParameterValue>>
>;