import type { AnalysisCategory, MetricParameterConfig } from "../types";

export const DEFAULT_WEIGHT = 5;

const createStandardIntRangeParameters = (): MetricParameterConfig[] => [
  {
    key: "hardRequirementRange",
    label: "Hard Requirement Range",
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
    key: "hardRequirementRange",
    label: "Hard Requirement Range",
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
    key: "hardRequirementRange",
    label: "Hard Requirement Range",
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
        name: "Total Git Branches (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "First Commit Date",
        parameters: createStandardDateRangeParameters(),
      },
      {
        name: "Last Commit Date (not rdy)",
        parameters: createStandardDateRangeParameters(),
      },
      {
        name: "Total Commits",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Average Commits Per Month (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Average Commit Size (not rdy)",
        parameters: createStandardIntRangeParameters(),
        tooltipText: "In lines of code, excluding generated and boilerplate files",
      },
      {
        name: "Total Lines of Code (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Total Lines of Code (filtered) ⭐ (not rdy)",
        parameters: createStandardIntRangeParameters(),
        tooltipText: "Excluding generated and boilerplate files",
      },
      {
        name: "Total Files (not rdy)",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Total Files (filtered) ⭐ (not rdy)",
        parameters: createStandardIntRangeParameters(),
        tooltipText: "Excluding generated and boilerplate files",
      },
      {
        name: "Technology Stack Count (not rdy)",
        parameters: createStandardIntRangeParameters(),
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
        name: "Estimated README Quality ⭐ (not rdy)",
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
        name: "Estimated Commit Naming Consistency ⭐ (not rdy)",
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