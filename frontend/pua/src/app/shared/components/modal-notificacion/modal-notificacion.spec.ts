import { describe, it, expect, beforeEach } from 'vitest';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ɵresolveComponentResources as resolveComponentResources } from '@angular/core';
import { ModalNotificacion } from './modal-notificacion';

describe('ModalNotificacion', () => {
  let component: ModalNotificacion;
  let fixture: ComponentFixture<ModalNotificacion>;

  beforeEach(async () => {
    await resolveComponentResources(() => Promise.resolve('<div></div>'));
    await TestBed.configureTestingModule({
      imports: [ModalNotificacion],
    }).compileComponents();

    fixture = TestBed.createComponent(ModalNotificacion);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
