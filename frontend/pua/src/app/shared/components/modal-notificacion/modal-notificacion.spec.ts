import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalNotificacion } from './modal-notificacion';

describe('ModalNotificacion', () => {
  let component: ModalNotificacion;
  let fixture: ComponentFixture<ModalNotificacion>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalNotificacion],
    }).compileComponents();

    fixture = TestBed.createComponent(ModalNotificacion);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
