import type { AnalysisCategory, MetricParameterConfig } from "../types/types";

export const DEFAULT_WEIGHT = 5;

const createStandardIntRangeParameters = (): MetricParameterConfig[] => [
  {
    key: "requirementRange",
    label: "Requirement Range",
    type: "int-range",
  },
  {
    key: "recommendedRange",
    label: "Recommended Range",
    type: "int-range",
  },
  {
    key: "idealRange",
    label: "Ideal Range",
    type: "int-range",
  },
];

const createStandardDateRangeParameters = (): MetricParameterConfig[] => [
  {
    key: "requirementRange",
    label: "Requirement Range",
    type: "date-range",
  },
  {
    key: "recommendedRange",
    label: "Recommended Range",
    type: "date-range",
  },
  {
    key: "idealRange",
    label: "Ideal Range",
    type: "date-range",
  },
];

const createPercentageRangeParameters = (): MetricParameterConfig[] => [
  {
    key: "requirementRange",
    label: "Requirement Range",
    type: "percentage-range",
  },
  {
    key: "recommendedRange",
    label: "Recommended Range",
    type: "percentage-range",
  },
  {
    key: "idealRange",
    label: "Ideal Range",
    type: "percentage-range",
  },
];

export const ANALYSIS_CATEGORIES: AnalysisCategory[] = [
  {
    title: "General",
    items: [
      {
        name: "Total Branches (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "First Commit Date",
        parameters: createStandardDateRangeParameters(),
      },
      {
        name: "Last Commit Date",
        parameters: createStandardDateRangeParameters(),
      },
      {
        name: "Total Commits",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Average Commits Per Month",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Average Commit Size (not rdy)",
        parameters: createStandardIntRangeParameters(),
        tooltipText: "In lines of text",
      },
      {
        name: "Average Commit Size (filtered) (not rdy)",
        parameters: createStandardIntRangeParameters(),
        tooltipText: "Outlier commits with 4x or more lines of text than "+
        "the average will not be counted",
      },
      {
        name: "Median Commit Size (not rdy)",
        parameters: createStandardIntRangeParameters(),
        tooltipText: "In lines of text",
      },
      {
        name: "Total Lines of Code",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Total Lines of Code (filtered) ⭐ (not rdy)",
        parameters: createStandardIntRangeParameters(),
        tooltipText: "Excluding generated and boilerplate files",
      },
      {
        name: "Total Files",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Total Files (filtered) ⭐ (not rdy)",
        parameters: createStandardIntRangeParameters(),
        tooltipText: "Excluding generated and boilerplate files",
      },
      {
        name: "Languages Used (not rdy)",
        parameters: createStandardIntRangeParameters(),
        tooltipText: "Includes non-programming languages (HTML, CSS, Shell etc.)",
      },
      {
        name: "Languages Used (filtered) (not rdy)",
        parameters: createStandardIntRangeParameters(),
        tooltipText: "Includes only the programming languages (Python, JavaScript, C#, Java etc.)",
      },
      {
        name: "Total Forks (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Stars (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
    ],
  },
  {
    title: "Collaboration",
    items: [
      {
        name: "Total Contributors (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Total Pull Requests (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Pull Request Acceptance Rate",
        parameters: createPercentageRangeParameters(),
      },
      {
        name: "Average Pull Request Reviewer Count (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Total Issues (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Issue Resolution Rate (not rdy)",
        parameters: createPercentageRangeParameters(),
      },
    ],
  },
  {
    title: "Documentation",
    items: [
      {
        name: "README Total Commits (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "README Length (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Estimated README Quality ⭐",
        parameters: createPercentageRangeParameters(),
      },
      {
        name: "GitHub Wiki Total Commits",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "GitHub Wiki Length (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Estimated GitHub Wiki Quality ⭐ (not rdy)",
        parameters: createPercentageRangeParameters(),
      },
    ],
  },
  {
    title: "Code & Repository Quality",
    items: [
      { 
        name: "Estimated Commit Naming Quality ⭐ (not rdy)",
        parameters: createPercentageRangeParameters(),
      },
      { 
        name: "Estimated Commit Message and Code Change Alignment ⭐ (not rdy)",
        parameters: createPercentageRangeParameters(),
      },
      { 
        name: "Estimated Consistency of Class, Function, Variable, and File Naming ⭐ (not rdy)",
        parameters: createPercentageRangeParameters(),
      },
      { 
        name: "Estimated Code Duplication ⭐ (not rdy)",
        parameters: createPercentageRangeParameters(),
      },
      { 
        name: "Estimated Frontend Test Coverage ⭐ (not rdy)",
        parameters: createPercentageRangeParameters(),
      },
      { 
        name: "Estimated Backend Test Coverage ⭐ (not rdy)",
        parameters: createPercentageRangeParameters(),
      },
      { 
        name: "Estimated File Architecture Quality ⭐ (not rdy)",
        parameters: createPercentageRangeParameters(),
      },
      { 
        name: "Estimated AI-Generated Code ⭐ (not rdy)",
        parameters: createPercentageRangeParameters(),
      },
    ],
  },
  {
    title: "HR Metrics",
    items: [
      { 
        name: "Estimated Project Summary and CV Match ⭐ (not rdy)",
        parameters: createPercentageRangeParameters(),
      },
      { 
        name: "Estimated Technology Stack and CV Match ⭐ (not rdy)",
        parameters: createPercentageRangeParameters(),
      },
    ],
  },
];