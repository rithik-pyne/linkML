export interface Mutation {
  mutation_id: string;
  gene_symbol: string;
  mutation_type: string;
  mutation_hgvs: string;
  vaf_percent: number;
  tumor_fraction_percent: number | null;
  actionable_mutation: boolean;
  is_primary_driver: boolean;
  is_acquired_resistance: boolean;
  resistance_mutation: boolean;
  detection_timepoint: string;
  test_date: string;
  specimen_source: string;
  ngs_panel_name: string;
}

export interface PDL1Status {
  tps_percent: number;
  antibody_clone: string;
  test_date: string;
}

export interface LatestNGSTest {
  molecular_test_id: string;
  test_date: string;
  specimen_source: string;
  ngs_panel_name: string;
  ngs_panel_version: string;
  mean_coverage_depth: number;
}

export interface MolecularProfile {
  patient_id: string;
  primary_driver_mutation: Mutation;
  co_mutations: Mutation[];
  resistance_mutations: Mutation[];
  pdl1_status: PDL1Status | null;
  actionable_mutations_count: number;
  latest_ngs_test: LatestNGSTest;
}