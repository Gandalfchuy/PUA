import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProcesoReeducacion } from './proceso-reeducacion';

describe('ProcesoReeducacion', () => {
  let component: ProcesoReeducacion;
  let fixture: ComponentFixture<ProcesoReeducacion>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProcesoReeducacion],
    }).compileComponents();

    fixture = TestBed.createComponent(ProcesoReeducacion);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
