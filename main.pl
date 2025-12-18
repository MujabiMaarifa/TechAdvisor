:- dynamic has_symptom/1.
:- dynamic derived_problem/1.
:- discontiguous diagnose/1.

% ==================================================
% SYMPTOMS
% ==================================================
symptom(no_power).
symptom(slow_performance).
symptom(overheating).
symptom(no_internet).
symptom(blue_screen).
symptom(strange_noise).
symptom(battery_not_charging).
symptom(screen_flickering).
symptom(keyboard_not_working).
symptom(mouse_not_working).
symptom(app_crashing).
symptom(storage_full).
symptom(os_not_booting).
symptom(wifi_disconnects).
symptom(system_freezing).

% ==================================================
% SINGLE SYMPTOM PROBLEMS
% ==================================================
problem(power_supply_failure) :- has_symptom(no_power).
problem(wifi_adapter_fault) :- has_symptom(wifi_disconnects).
problem(network_driver_issue) :- has_symptom(no_internet).
problem(overheating_issue) :- has_symptom(overheating).
problem(malware_infection) :- has_symptom(slow_performance).
problem(ram_issue) :- has_symptom(blue_screen).
problem(battery_issue) :- has_symptom(battery_not_charging).
problem(display_driver_issue) :- has_symptom(screen_flickering).
problem(input_device_failure) :- has_symptom(keyboard_not_working).
problem(input_device_failure) :- has_symptom(mouse_not_working).
problem(hard_disk_full) :- has_symptom(storage_full).
problem(os_boot_issue) :- has_symptom(os_not_booting).
problem(hardware_noise_issue) :- has_symptom(strange_noise).
problem(system_freezing_issue) :- has_symptom(system_freezing).
problem(app_crashing_issue) :- has_symptom(app_crashing).

% ==================================================
% MULTI-STEP FORWARD CHAINING RULES
% ==================================================
forward_chain_all :-
    has_symptom(overheating),
    has_symptom(system_freezing),
    \+ derived_problem(system_freeze_issue),
    assertz(derived_problem(system_freeze_issue)),
    fail.
forward_chain_all :-
    has_symptom(no_power),
    has_symptom(battery_not_charging),
    \+ derived_problem(power_issue),
    assertz(derived_problem(power_issue)),
    fail.
forward_chain_all :-
    has_symptom(no_internet),
    has_symptom(wifi_disconnects),
    \+ derived_problem(network_connectivity_issue),
    assertz(derived_problem(network_connectivity_issue)),
    fail.
forward_chain_all :-
    has_symptom(strange_noise),
    has_symptom(blue_screen),
    \+ derived_problem(hardware_failure_risk),
    assertz(derived_problem(hardware_failure_risk)),
    fail.
forward_chain_all :-
    has_symptom(storage_full),
    has_symptom(slow_performance),
    \+ derived_problem(storage_overload),
    assertz(derived_problem(storage_overload)),
    fail.
forward_chain_all.

% ==================================================
% BACKWARD CHAINING (Single-best diagnosis)
% ==================================================
diagnose(power_supply_failure) :- problem(power_supply_failure), !.
diagnose(overheating_issue) :- problem(overheating_issue), !.
diagnose(malware_infection) :- problem(malware_infection), !.
diagnose(network_driver_issue) :- problem(network_driver_issue), !.
diagnose(wifi_adapter_fault) :- problem(wifi_adapter_fault), !.
diagnose(unknown_problem).

% ==================================================
% MULTIPLE DIAGNOSES
% ==================================================
diagnose_all(Problem) :- problem(Problem).

% ==================================================
% CONFLICT RESOLUTION BY HIGHEST CONFIDENCE
% ==================================================
select_highest_confidence(Problem, MaxC) :-
    findall([P,C], (diagnose_all(P), confidence(P,C)), L),
    sort(2, @>=, L, Sorted),
    Sorted = [[Problem,MaxC]|_].

% ==================================================
% SOLUTIONS
% ==================================================
solution(power_supply_failure, 'Check power cable, replace power supply, or test another socket.').
solution(wifi_adapter_fault, 'Restart router, reset WiFi adapter, or replace adapter.').
solution(network_driver_issue, 'Reinstall or update network drivers.').
solution(overheating_issue, 'Clean cooling fans, replace thermal paste, and improve airflow.').
solution(malware_infection, 'Run antivirus scan and remove suspicious software.').
solution(ram_issue, 'Reseat or replace faulty RAM module.').
solution(battery_issue, 'Replace battery or check charger.').
solution(display_driver_issue, 'Update or reinstall display drivers.').
solution(input_device_failure, 'Reconnect or replace keyboard or mouse.').
solution(hard_disk_full, 'Delete unnecessary files or upgrade storage.').
solution(os_boot_issue, 'Repair OS boot files or reinstall operating system.').
solution(hardware_noise_issue, 'Check fans and hard drive for mechanical failure.').
solution(system_freezing_issue, 'Check system cooling and memory usage.').
solution(app_crashing_issue, 'Update or reinstall the application.').
solution(system_freeze_issue, 'Check system logs, clean overheating components, and update drivers.').
solution(power_issue, 'Check power supply and battery; replace if necessary.').
solution(network_connectivity_issue, 'Check router, network drivers, and adapters.').
solution(hardware_failure_risk, 'Investigate potential hardware faults: RAM, HDD, fans.').
solution(storage_overload, 'Clean disk space and remove unnecessary files.').

% ==================================================
% CONFIDENCE SCORES
% ==================================================
confidence(power_supply_failure, 0.9).
confidence(overheating_issue, 0.85).
confidence(malware_infection, 0.8).
confidence(network_driver_issue, 0.75).
confidence(wifi_adapter_fault, 0.7).
confidence(ram_issue, 0.8).
confidence(battery_issue, 0.75).
confidence(display_driver_issue, 0.7).
confidence(input_device_failure, 0.65).
confidence(hard_disk_full, 0.85).
confidence(os_boot_issue, 0.9).
confidence(hardware_noise_issue, 0.6).
confidence(system_freezing_issue, 0.7).
confidence(app_crashing_issue, 0.75).
confidence(system_freeze_issue, 0.8).
confidence(power_issue, 0.85).
confidence(network_connectivity_issue, 0.8).
confidence(hardware_failure_risk, 0.7).
confidence(storage_overload, 0.75).
