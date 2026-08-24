import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Agresores } from './agresores';

describe('Agresores', () => {
  let component: Agresores;
  let fixture: ComponentFixture<Agresores>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Agresores],
    }).compileComponents();

    fixture = TestBed.createComponent(Agresores);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
