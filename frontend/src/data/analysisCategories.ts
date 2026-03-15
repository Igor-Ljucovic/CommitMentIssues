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

export const ANALYSIS_CATEGORIES: AnalysisCategory[] = [
  {
    title: "General",
    items: [
      {
        name: "Total Repositories",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Repository Creation Date",
        parameters: createStandardDateRangeParameters(),
      },
      {
        name: "Last Commit Date",
        parameters: createStandardDateRangeParameters(),
      },
      {
        name: "Total Commits",
        parameters: createStandardIntRangeParameters(),
        subItems: [
          {
            name: "Average Commit Frequency (per month)",
            parameters: createStandardIntRangeParameters(),
          },
          {
            name: "Average Commit Size",
            parameters: createStandardIntRangeParameters(),
            tooltipText:
              "In lines of code, excluding generated and boilerplate files",
          },
        ],
      },
      {
        name: "Total Git Branches",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Total Lines of Code",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Total Lines of Code (filtered)",
        parameters: createStandardIntRangeParameters(),
        tooltipText: "Excluding generated and boilerplate files",
      },
      {
        name: "Total Files",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Total Files (filtered)",
        parameters: createStandardIntRangeParameters(),
        tooltipText: "Excluding generated and boilerplate files",
      },
      {
        name: "Total Forks",
        parameters: createStandardIntRangeParameters(),
      },
      {
        name: "Stars",
        parameters: createStandardIntRangeParameters(),
      },
    ],
  },
  {
    title: "Collaboration",
    items: [
      { name: "Contributor Count" },
      { name: "Branch Overview" },
      { name: "Pull Request Acceptance Rate" },
    ],
  },
  {
    title: "Documentation",
    items: [
      { name: "README and Wiki Presence & Quality" },
      { name: "Project Summary and CV Match" },
    ],
  },
  {
    title: "Consistency",
    items: [
      { name: "Commit Naming Consistency" },
      { name: "Commit Message and Code Change Alignment" },
      {
        name: "Consistency of Class, Function, Variable, and File Naming",
      },
    ],
  },
  {
    title: "Architecture",
    items: [
      { name: "Software Architecture Overview" },
      { name: "Project Summary and Functional Match" },
      { name: "Code Duplication" },
      { name: "Tests and Test Coverage" },
    ],
  },
  {
    title: "AI Code Analysis",
    items: [
      { name: "Technology Stack Match with CV" },
      { name: "Commit Message and Code Change Alignment (AI)" },
      { name: "Naming and Project Structure Consistency (AI)" },
      { name: "Project Summary and CV Match (AI)" },
      { name: "Estimated AI-Generated Code Percentage" },
    ],
  },
];